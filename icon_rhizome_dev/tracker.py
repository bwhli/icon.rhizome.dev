import asyncio
import json

import orjson

from icon_rhizome_dev.constants import TRACKER_API_ENDPOINT
from icon_rhizome_dev.http_client import HttpClient
from icon_rhizome_dev.icx_async import IcxAsync
from icon_rhizome_dev.models.icx import IcxTransaction
from icon_rhizome_dev.models.tracker import TrackerAddress
from icon_rhizome_dev.redis_client import RedisClient


class Tracker:
    """
    A class for making requests to the ICON Community Tracker API.
    """

    @classmethod
    async def get_address_details(cls, address: str) -> dict:
        """
        Returns details about an ICX address.

        Args:
            address: An ICX address.
        """
        response = await HttpClient.get(f"{TRACKER_API_ENDPOINT}/addresses/details/{address}")  # fmt: skip
        data = response.json()
        address_details = TrackerAddress(**data)
        return address_details

    @classmethod
    async def get_token_addresses(cls, address: str) -> list:
        """
        Returns a list of tokens owned by an ICX address.

        Args:
            address: An ICX address.
        """
        response = await HttpClient.get(f"{TRACKER_API_ENDPOINT}/addresses/token-addresses/{address}")  # fmt: skip
        token_addresses = response.json()
        return token_addresses

    @classmethod
    async def get_token_transfers(
        cls,
        from_address: str,
        to_address: str,
        limit: int = 100,
    ) -> list:
        url = f"{TRACKER_API_ENDPOINT}/transactions/token-transfers?limit={limit}&from={from_address}&to={to_address}"
        r = await HttpClient.get(url)
        token_transfers = r.json()
        return token_transfers

    @classmethod
    async def get_token_balances(cls, address: str, block_number: int = 0):
        token_addresses = await cls.get_token_addresses(address)
        token_balances = await asyncio.gather(*[IcxAsync.get_token_balance(address, token_address) for token_address in token_addresses])  # fmt: skip
        return token_balances

    @classmethod
    async def get_block_from_timestamp(
        cls,
        timestamp: int,
        block_number_only: bool = False,
    ) -> int:
        """
        Returns block height for the provided timestamp.

        Args:
            timestamp (int): Unix timestamp in seconds (must be greater than 1516819217)

        Returns:
            int: Block height for the provided timestamp.
        """
        response = await HttpClient.get(f"{TRACKER_API_ENDPOINT}/blocks/timestamp/{timestamp * 1000000}/")  # fmt: skip

        if response.status_code == 200:
            block = response.json()
            if block_number_only is True:
                return block["number"]
            return block
        else:
            return None

    @classmethod
    async def get_iscore_claimed(cls, tx_hash: str) -> int:
        response = await HttpClient.get(f"{TRACKER_API_ENDPOINT}/logs?transaction_hash={tx_hash}")  # fmt: skip
        data = response.json()
        log_data = json.loads(data[0]["data"])
        log_data = [int(v, 16) for v in log_data]
        iscore_claimed = int(log_data[0])
        return iscore_claimed

    @classmethod
    async def get_api_endpoint(cls, address: str) -> str:
        url = f"{TRACKER_API_ENDPOINT}/governance/preps/{address}"
        r = await HttpClient.get(url)
        data = r.json()
        validator = data[0]
        api_endpoint = validator.get("api_endpoint")
        return api_endpoint

    @classmethod
    async def get_transaction(cls, tx_hash: str) -> IcxTransaction:
        """
        Returns details about an ICX transaction.

        Args:
            tx_hash: An ICX transaction hash.
        """
        response = await HttpClient.get(f"{TRACKER_API_ENDPOINT}/transaction/details/{tx_hash}")  # fmt: skip
        transaction = IcxTransaction(**response)
        return transaction

    @classmethod
    async def get_transactions(
        cls,
        limit: int = 100,
        skip: int = 0,
        sort: str = "desc",
        from_address: str = None,
        to_address: str = None,
        type: str = None,
        block_number: int = None,
        start_block_number: int = None,
        end_block_number: int = None,
        method: str = None,
    ) -> list[IcxTransaction]:
        """
        Returns a list of ICX transactions.
        """
        # Build query parameters.
        query_params = []

        if from_address is not None:
            query_params.append(f"from={from_address}")
        if to_address is not None:
            query_params.append(f"to={to_address}")
        if type is not None:
            query_params.append(f"type={type}")
        if block_number is not None:
            query_params.append(f"block_number={block_number}")
        if start_block_number is not None:
            query_params.append(f"start_block_number={start_block_number}")
        if end_block_number is not None:
            query_params.append(f"end_block_number={end_block_number}")
        if method is not None:
            query_params.append(f"method={method}")

        url = f"{TRACKER_API_ENDPOINT}/transactions?limit={limit}&skip={skip}&sort={sort}"  # fmt: skip

        if len(query_params) == 1:
            url = f"{url}&{query_params[0]}"
        elif len(query_params) > 1:
            url = f"{url}&{'&'.join(query_params)}"

        response = await HttpClient.get(url)

        if response.status_code == 200:
            transactions = [IcxTransaction(**transaction) for transaction in response.json()]  # fmt: skip
            return transactions
        else:
            return None

    @classmethod
    async def get_validator_node_hostnames(cls):
        # Return cached data from Redis if it exists.
        REDIS_KEY = "VALIDATOR_NODE_HOSTNAMES"
        cached_data = await RedisClient.get(REDIS_KEY)
        if cached_data is not None:
            return orjson.loads(cached_data)

        # Fetch data from Tracker API if there is no cached data.
        url = f"{TRACKER_API_ENDPOINT}/governance/preps"
        r = await HttpClient.get(url)
        data = r.json()
        hostnames = {
            validator.get("address"): {
                "api_endpoint": validator.get("api_endpoint"),
                "p2p_endpoint": validator.get("p2p_endpoint"),
            }
            for validator in data
        }

        # Store data in Redis for 3600s.
        await RedisClient.set(REDIS_KEY, orjson.dumps(hostnames), 3600)
        return hostnames

    @classmethod
    async def is_approved_voter(cls, address: str):
        url = f"{TRACKER_API_ENDPOINT}/governance/delegations/{address}?skip=0&limit=100"  # fmt: skip

        response = await HttpClient.get(url)

        if response.status_code == 200:
            delegations = response.json()

            total_delegation_value = sum([delegation["value"] for delegation in delegations])  # fmt: skip

            for delegation in delegations:
                if delegation["prep"] == "hx4a43790d44b07909d20fbcc233548fc80f7a4067":
                    if delegation["value"] / total_delegation_value >= 0.2:
                        return True

        return False
