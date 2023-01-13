import json

from icon_rhizome_dev.constants import TRACKER_API_ENDPOINT
from icon_rhizome_dev.http import Http
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
        response = await Http.get(f"{TRACKER_API_ENDPOINT}/addresses/token-addresses/{address}")  # fmt: skip
        return response

    @staticmethod
    async def get_address_tokens(address: str) -> list:
        """
        Returns a list of tokens owned by an ICX address.

        Args:
            address: An ICX address.
        """
        response = await Http.get(f"{TRACKER_API_ENDPOINT}/addresses/token-addresses/{address}")  # fmt: skip
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
        response = await Http.get(f"{TRACKER_API_ENDPOINT}/blocks/timestamp/{timestamp * 1000000}/")  # fmt: skip

        if response.status_code == 200:
            block = response.json()
            if block_number_only is True:
                return block["number"]
            return block
        else:
            return None

    @staticmethod
    async def get_iscore_claimed(tx_hash: str) -> int:
        response = await Http.get(f"{TRACKER_API_ENDPOINT}/logs?transaction_hash={tx_hash}")  # fmt: skip
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
        response = await Http.get(f"{TRACKER_API_ENDPOINT}/transaction/details/{tx_hash}")  # fmt: skip
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

        response = await Http.get(url)

        if response.status_code == 200:
            transactions = [IcxTransaction(**transaction) for transaction in response.json()]  # fmt: skip
            return transactions
        else:
            return None

    @staticmethod
    async def get_validators(calculate_rewards: bool = True):
        url = "https://tracker.icon.community/api/v1/governance/preps"
        response = await Http.get(url)
        import json

        for validator in response:

            print(json.dumps(validator, indent=4))
        validators = [Validator(**validator) for validator in response]
        if calculate_rewards is True:
            icx_usd_price = Icx.get_icx_usd_price()
        return validators
