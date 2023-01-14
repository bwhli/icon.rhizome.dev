import httpx

from icon_rhizome_dev.icx import Icx
from icon_rhizome_dev.models.icx import IcxValidator
from icon_rhizome_dev.utils import Utils


class IcxAsync(Icx):
    def __init__(self) -> None:
        pass

    @classmethod
    async def get_cps_validator_addresses(cls, height: int = None):
        result = await cls.call(
            "cx9f4ab72f854d3ccdc59aa6f2c3e2215dd62e879f",
            "get_PReps",
        )
        validators = [validator["address"] for validator in result]
        return validators

    @classmethod
    async def get_icx_usd_price(cls, height: int = None):
        params = {"_symbol": "ICX"}
        result = await cls.call(
            "cx087b4164a87fdfb7b714f3bafe9dfb050fd6b132",
            "get_ref_data",
            params,
        )
        icx_usd_price = Utils.hex_to_int(result["rate"]) / 1000000000
        return icx_usd_price

    @classmethod
    async def get_network_info(cls, height: int = None):
        result = await cls.call(cls.CHAIN_CONTRACT, "getNetworkInfo")
        for k, v in result.items():
            if isinstance(v, str):
                result[k] = Utils.hex_to_int(v)
        for k, v in result["rewardFund"].items():
            if isinstance(v, str):
                result["rewardFund"][k] = Utils.hex_to_int(v)
        return result

    @classmethod
    async def get_validators(
        cls,
        start_ranking: int = 1,
        end_ranking: int = 200,
    ):
        params = {
            "startRanking": Utils.int_to_hex(start_ranking),
            "endRanking": Utils.int_to_hex(end_ranking),
        }
        result = await cls.call(cls.CHAIN_CONTRACT, "getPReps", params)
        validators = [IcxValidator(**validator) for validator in result["preps"]]
        return validators

    @classmethod
    async def call(
        cls,
        to_address: str,
        method: str,
        params: dict = {},
        height: int | None = None,
    ):
        payload = {
            "jsonrpc": "2.0",
            "id": 1234,
            "method": "icx_call",
            "params": {
                "to": to_address,
                "dataType": "call",
                "data": {
                    "method": method,
                    "params": params,
                    "height": height,
                },
            },
        }
        result = await cls._make_api_request(payload)
        return result

    @classmethod
    async def _make_api_request(cls, payload):
        async with httpx.AsyncClient() as client:
            r = await client.post(f"{cls.ICON_API_ENDPOINT}/api/v3", json=payload)
        data = r.json()
        return data["result"]
