import json

from icon_rhizome_dev.constants import TRACKER_API_ENDPOINT
from icon_rhizome_dev.http_client import HttpClient
from icon_rhizome_dev.models.tracker import (
    TrackerAddress,
    TrackerContractDetails,
    TrackerLog,
    TrackerTokenTransfer,
    TrackerTransaction,
)


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
        r = await HttpClient.get(f"{TRACKER_API_ENDPOINT}/addresses/details/{address}")
        data = r.json()
        print(data)
        address_details = TrackerAddress(**data)
        return address_details

    @classmethod
    async def get_contract_details(cls, contract_address: str):
        r = await HttpClient.get(f"{TRACKER_API_ENDPOINT}/contracts/{contract_address}")
        data = r.json()
        contract_details = TrackerContractDetails(**data)
        return contract_details

    @classmethod
    async def get_logs(
        cls,
        limit: int = 100,
        skip: int = 0,
        address: str = None,
        block_number: int = None,
        start_block_number: int = None,
        end_block_number: int = None,
        tx_hash: str = None,
        method: str = None,
    ) -> list[TrackerTransaction]:
        """
        Returns a list of ICX transactions.
        """
        # Build query parameters.
        query_args = []

        if address is not None:
            query_args.append(f"address={address}")
        if type is not None:
            query_args.append(f"type={type}")
        if block_number is not None:
            query_args.append(f"block_number={block_number}")
        if start_block_number is not None:
            query_args.append(f"block_start={start_block_number}")
        if end_block_number is not None:
            query_args.append(f"block_end={end_block_number}")
        if tx_hash is not None:
            query_args.append(f"transaction_hash={tx_hash}")
        if method is not None:
            query_args.append(f"method={method}")

        url = f"{TRACKER_API_ENDPOINT}/logs?limit={limit}&skip={skip}"

        if len(query_args) == 1:
            url = f"{url}&{query_args[0]}"
        elif len(query_args) > 1:
            url = f"{url}&{'&'.join(query_args)}"

        r = await HttpClient.get(url)

        if r.status_code == 200:
            logs = [TrackerLog(**log) for log in r.json()]
            return logs
        else:
            return None

    @classmethod
    async def get_token_addresses(cls, address: str) -> list:
        """
        Returns a list of tokens owned by an ICX address.

        Args:
            address: An ICX address.
        """
        r = await HttpClient.get(f"{TRACKER_API_ENDPOINT}/addresses/token-addresses/{address}")  # fmt: skip
        token_addresses = r.json()
        return token_addresses

    @classmethod
    async def get_token_transfers(
        cls,
        limit: int = 100,
        skip: int = 0,
        from_address: str = None,
        to_address: str = None,
        type: str = None,
        block_number: int = None,
        start_block_number: int = None,
        end_block_number: int = None,
        token_contract_address: str = None,
        transaction_hash: str = None,
    ) -> list[TrackerTokenTransfer]:

        query_args = []

        if limit is not None:
            query_args.append(f"limit={limit}")
        if skip is not None:
            query_args.append(f"skip={skip}")
        if from_address is not None:
            query_args.append(f"from={from_address}")
        if to_address is not None:
            query_args.append(f"to={to_address}")
        if type is not None:
            query_args.append(f"type={type}")
        if block_number is not None:
            query_args.append(f"block_number={block_number}")
        if start_block_number is not None:
            query_args.append(f"start_block_number={start_block_number}")
        if end_block_number is not None:
            query_args.append(f"end_block_number={end_block_number}")
        if token_contract_address is not None:
            query_args.append(f"token_contract_address={token_contract_address}")
        if transaction_hash is not None:
            query_args.append(f"transaction_hash={transaction_hash}")

        r = await HttpClient.get(
            cls._build_url("/transactions/token-transfers", query_args)
        )

        if r.status_code == 200:
            token_transfers = [
                TrackerTokenTransfer(**token_transfer) for token_transfer in r.json()
            ]
            return token_transfers
        else:
            return []

    @classmethod
    async def get_block_from_timestamp(
        cls,
        timestamp: int,
        block_number_only: bool = False,
    ) -> int:
        """
        Returns block height for the provided timestamp.

        Args:
            timestamp (int): Unix timestamp in microseconds.

        Returns:
            int: Block height for the provided timestamp.
        """
        r = await HttpClient.get(
            f"{TRACKER_API_ENDPOINT}/blocks/timestamp/{timestamp}/"
        )

        print(r.json())

        if r.status_code == 200:
            block = r.json()
            if block_number_only is True:
                return block["number"]
            return block
        else:
            return None

    @classmethod
    async def get_iscore_claimed(cls, tx_hash: str) -> int:
        r = await HttpClient.get(
            f"{TRACKER_API_ENDPOINT}/logs?transaction_hash={tx_hash}"
        )
        data = r.json()
        log_data = json.loads(data[0]["data"])
        log_data = [int(v, 16) for v in log_data]
        iscore_claimed = int(log_data[0])
        return iscore_claimed

    @classmethod
    async def get_api_endpoint(cls, address: str) -> str:
        url = f"{TRACKER_API_ENDPOINT}/preps/{address}"
        r = await HttpClient.get(url)
        data = r.json()
        validator = data[0]
        api_endpoint = validator.get("api_endpoint")
        return api_endpoint

    @classmethod
    async def get_transaction(cls, tx_hash: str) -> TrackerTransaction:
        """
        Returns details about an ICX transaction.

        Args:
            tx_hash: An ICX transaction hash.
        """
        r = await HttpClient.get(f"{TRACKER_API_ENDPOINT}/transactions/details/{tx_hash}")  # fmt: skip
        transaction = TrackerTransaction(**r.json())
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
        get_all: bool = False,
    ) -> list[TrackerTransaction]:
        """
        Returns a list of ICX transactions.
        """

        query_args = {}
        query_args["limit"] = limit
        query_args["skip"] = skip
        query_args["sort"] = sort
        query_args["from"] = from_address
        query_args["to"] = to_address
        query_args["type"] = type
        query_args["block_number"] = block_number
        query_args["start_block_number"] = start_block_number
        query_args["end_block_number"] = end_block_number
        query_args["method"] = method

        r = await HttpClient.get(cls._build_url("/transactions", query_args))

        if r.status_code == 200:
            transactions = [
                TrackerTransaction(**transaction) for transaction in r.json()
            ]
            return transactions
        else:
            return None

    @classmethod
    async def get_validator_node_hostnames(cls):
        # Return cached data from Redis if it exists.
        REDIS_KEY = "VALIDATOR_NODE_HOSTNAMES"
        cached_data = await RedisClient.get(REDIS_KEY)
        if cached_data is not None:
            return json.loads(cached_data)

        # Fetch data from Tracker API if there is no cached data.
        url = f"{TRACKER_API_ENDPOINT}/preps"
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
        await RedisClient.set(REDIS_KEY, json.dumps(hostnames), 3600)
        return hostnames

    @classmethod
    async def is_approved_voter(cls, address: str):
        url = f"{TRACKER_API_ENDPOINT}/delegations/{address}?skip=0&limit=100"
        r = await HttpClient.get(url)
        if r.status_code == 200:
            delegations = r.json()
            total_delegation_value = sum(
                [delegation["value"] for delegation in delegations]
            )
            for delegation in delegations:
                if (
                    delegation["prep_address"]
                    == "hx4a43790d44b07909d20fbcc233548fc80f7a4067"
                ):
                    if delegation["value"] / total_delegation_value >= 0.2:
                        return True
        return False

    @staticmethod
    def _build_url(path: str, query_args: list[str]):
        url = f"{TRACKER_API_ENDPOINT}{path}?"
        if len(query_args) == 1:
            url = f"{url}&{query_args[0]}"
        elif len(query_args) > 1:
            url = f"{url}&{'&'.join(query_args)}"
        return url

    @staticmethod
    async def _get_iteration_count(url: str, limit: int):
        path = url.strip(TRACKER_API_ENDPOINT)
        await HttpClient.get(
            f"https://tracker.v2.mainnet.sng.vultr.icon.community{path}"
        )
        return

    @staticmethod
    def _generate_query_string(query_args: dict[str, str]) -> str:
        """
        Returns a valid query string from a dict containing query key to query value mappings.

        Args:
            query_args: A dictionary of key, value mappings for the query string.
        """
        # Filter out query key, value pairs if value is None.
        filted_query_args = {k: v for k, v in query_args.items() if v is not None}
        query_string = "?" + "&".join(
            [f"{k}={v}" for k, v in filted_query_args.items()]
        )
        return query_string
