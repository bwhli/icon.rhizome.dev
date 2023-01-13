import json

from icon_rhizome_dev.constants import TRACKER_API_ENDPOINT
from icon_rhizome_dev.http_client import HttpClient
from icon_rhizome_dev.icx import Icx
from icon_rhizome_dev.models.governance import Validator
from icon_rhizome_dev.models.icx import IcxAddress, IcxTransaction


class Tracker:
    """
    A class for making requests to the ICON Community Tracker API.
    """

    @staticmethod
    async def get_addresses():
        return

    @staticmethod
    async def get_address_details(address: str) -> dict:
        """
        Returns details about an ICX address.

        Args:
            address: An ICX address.
        """
        response = await HttpClient.get(f"{TRACKER_API_ENDPOINT}/addresses/token-addresses/{address}")  # fmt: skip
        return response

    @staticmethod
    async def get_address_tokens(address: str) -> list:
        """
        Returns a list of tokens owned by an ICX address.

        Args:
            address: An ICX address.
        """
        response = await HttpClient.get(f"{TRACKER_API_ENDPOINT}/addresses/token-addresses/{address}")  # fmt: skip
        return response

    @staticmethod
    async def get_block_from_timestamp(
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

    @staticmethod
    async def get_iscore_claimed(tx_hash: str) -> int:
        response = await HttpClient.get(f"{TRACKER_API_ENDPOINT}/logs?transaction_hash={tx_hash}")  # fmt: skip
        data = response.json()
        log_data = json.loads(data[0]["data"])
        log_data = [int(v, 16) for v in log_data]
        iscore_claimed = int(log_data[0])
        return iscore_claimed

    @staticmethod
    async def get_transaction(tx_hash: str) -> IcxTransaction:
        """
        Returns details about an ICX transaction.

        Args:
            tx_hash: An ICX transaction hash.
        """
        response = await HttpClient.get(f"{TRACKER_API_ENDPOINT}/transaction/details/{tx_hash}")  # fmt: skip
        transaction = IcxTransaction(**response)
        return transaction

    @staticmethod
    async def get_transactions(
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

    @staticmethod
    async def is_approved_voter(address: str):
        url = f"{TRACKER_API_ENDPOINT}/governance/delegations/{address}?skip=0&limit=100"  # fmt: skip
        approved_validators = [
            "hx4a43790d44b07909d20fbcc233548fc80f7a4067",  # RHIZOME
            "hx5da9e862b4e26e5ac486c1d70d9d63927ce35e1c",  # Studio Mirai
            "hxca60d4371ad90d624dc7119f81009d799c168aa1",  # FRAMD
            "hx2e7db537ca3ff73336bee1bab4cf733a94ae769b",  # Eye on ICON
            "hx9fa9d224306b0722099d30471b3c2306421aead7",  # Espanicon
            "hxfc56203484921c3b7a4dee9579d8614d8c8daaf5",  # Sudoblock
            "hx6f89b2c25c15f6294c79810221753131067ed3f8",  # Staky.io
        ]
        response = await HttpClient.get(url)

        if response.status_code == 200:
            valid_delegations = []  # Delegation to SM or RHIZOME
            delegations = response.json()
            total_delegation_value = sum([delegation["value"] for delegation in delegations])  # fmt: skip

            # Create a list of delegations to approved validators and represent more than 10% of total delegation.
            valid_delegations = [
                delegation
                for delegation in delegations
                if delegation["prep_address"] in approved_validators
                and delegation["value"] / total_delegation_value >= 0.1
            ]

            if len(valid_delegations) == len(approved_validators):
                return True

        return False
