from time import time
from typing import Union

from iconsdk.builder.call_builder import CallBuilder
from iconsdk.icon_service import IconService
from iconsdk.providers.http_provider import HTTPProvider
from requests.exceptions import ConnectionError

from icon_rhizome_dev.models.icx import IcxValidator
from icon_rhizome_dev.utils import Utils


class Icx:

    # Configure IconService object
    ICON_API_ENDPOINT = "https://api.icon.community"
    ICON_SERVICE = IconService(HTTPProvider(ICON_API_ENDPOINT, 3))

    # Core Contracts
    CHAIN_CONTRACT = "cx0000000000000000000000000000000000000000"
    GOVERNANCE_CONTRACT = "cx0000000000000000000000000000000000000001"

    def __init__(self) -> None:
        # self.last_block = self.get_block_height()
        pass

    @classmethod
    def call(
        cls,
        to_address: str,
        method: str,
        params={},
        height=None,
    ):
        call = CallBuilder(
            to=to_address,
            method=method,
            params=params,
            height=height,
        ).build()
        result = cls.ICON_SERVICE.call(call)
        return result

    @classmethod
    def get_block_height(cls):

        result = cls.ICON_SERVICE.get_block("latest")
        block_height = result["height"]
        return block_height

    @classmethod
    def get_icx_usd_price(
        cls,
        height: int = None,
    ) -> float:
        result = cls.call(
            "cx087b4164a87fdfb7b714f3bafe9dfb050fd6b132",
            "get_ref_data",
            {"_symbol": "ICX"},
            height=height,
        )
        icx_usd_price = Utils.hex_to_int(result["rate"]) / 1000000000
        return icx_usd_price

    @classmethod
    def get_validators(
        cls,
        height: int = None,
    ):
        result = cls.call(cls.CHAIN_CONTRACT, "getPReps", height=height)
        validators = result["preps"]

        keys_to_convert = {
            "irepUpdateBlockHeight": "irep_update_block_height",
            "lastHeight": "last_height",
            "nodeAddress": "node_address",
            "p2pEndpoint": "p2p_endpoint",
            "totalBlocks": "total_blocks",
            "validatedBlocks": "validated_blocks",
        }

        for validator in validators:
            for k, v in keys_to_convert.items():
                validator[v] = validator[k]

        validators = [IcxValidator(**validator) for validator in validators]
        return validators
