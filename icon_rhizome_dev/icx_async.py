import asyncio

import httpx
from httpx._exceptions import HTTPStatusError

from icon_rhizome_dev.constants import EXA
from icon_rhizome_dev.exceptions import FailedIcxCallException, OfflineNodeException
from icon_rhizome_dev.icx import Icx
from icon_rhizome_dev.models.icx import IcxDelegation, IcxValidator
from icon_rhizome_dev.redis_client import RedisClient
from icon_rhizome_dev.utils import Utils


class IcxAsync(Icx):
    def __init__(self) -> None:
        pass

    @classmethod
    async def get_balance(
        cls,
        address: str,
        in_icx=True,
        block_number: int = 0,
    ) -> int | float:
        payload = {
            "jsonrpc": "2.0",
            "id": 1234,
            "method": "icx_getBalance",
            "params": {
                "address": address,
            },
        }
        # Add height param to payload if height is provided.
        if block_number != 0:
            payload["params"]["height"] = Utils.int_to_hex(block_number)
        result = await cls._make_api_request(payload)
        balance = Utils.hex_to_int(result)
        if in_icx is True:
            balance = balance / 10**EXA
        return balance

    @classmethod
    async def get_last_block(cls, height_only=False):
        payload = {"jsonrpc": "2.0", "method": "icx_getLastBlock", "id": 1234}
        result = await cls._make_api_request(payload)
        if height_only is True:
            return result["height"]
        return result

    @classmethod
    async def get_delegation(
        cls,
        address: str,
        block_number: int = 0,
    ):
        params = {"address": address}
        result = await cls.call(
            cls.CHAIN_CONTRACT,
            "getDelegation",
            params,
            block_number=block_number,
        )
        delegations = [
            IcxDelegation(
                amount=delegation["value"],
                validator_address=delegation["address"],
                validator_name=await cls.get_validator_name(delegation["address"]),
            )
            for delegation in result["delegations"]
        ]
        return delegations

    @classmethod
    async def get_cps_validator_addresses(cls, block_number: int = 0):
        result = await cls.call(
            "cx9f4ab72f854d3ccdc59aa6f2c3e2215dd62e879f",
            "get_PReps",
            block_number=block_number,
        )
        validators = [validator["address"] for validator in result]
        return validators

    @classmethod
    async def get_icx_usd_price(cls, block_number: int = 0):
        params = {"_symbol": "ICX"}
        result = await cls.call(
            "cx087b4164a87fdfb7b714f3bafe9dfb050fd6b132",
            "get_ref_data",
            params,
            block_number=block_number,
        )
        icx_usd_price = Utils.hex_to_int(result["rate"]) / 1000000000
        return icx_usd_price

    @classmethod
    async def get_network_info(cls, block_number: int = 0):
        result = await cls.call(
            cls.CHAIN_CONTRACT,
            "getNetworkInfo",
            block_number=block_number,
        )
        for k, v in result.items():
            if isinstance(v, str):
                result[k] = Utils.hex_to_int(v)
        for k, v in result["rewardFund"].items():
            if isinstance(v, str):
                result["rewardFund"][k] = Utils.hex_to_int(v)
        return result

    @classmethod
    async def get_token_balance(
        cls,
        address: str,
        token_contract: str,
        block_number: int = 0,
    ) -> int:
        params = {"_owner": address}
        result = await IcxAsync.call(
            token_contract,
            "balanceOf",
            params,
            block_number=block_number,
        )
        return Utils.hex_to_int(result)

    @classmethod
    async def get_validator(
        cls,
        address: str,
        block_number: int = 0,
    ) -> IcxValidator:
        params = {"address": address}
        result = await cls.call(
            cls.CHAIN_CONTRACT, "getPRep", params, block_number=block_number
        )
        validator = IcxValidator(**result)
        return validator

    @classmethod
    async def get_validator_name(
        cls,
        address: str,
        block_number: int = 0,
    ) -> str:
        validator = await cls.get_validator(address, block_number=block_number)
        return validator.name

    @classmethod
    async def get_validators(
        cls,
        start_ranking: int = 1,
        end_ranking: int = 200,
        block_number: int = 0,
    ):
        params = {
            "startRanking": Utils.int_to_hex(start_ranking),
            "endRanking": Utils.int_to_hex(end_ranking),
        }
        result = await cls.call(
            cls.CHAIN_CONTRACT,
            "getPReps",
            params,
            block_number=block_number,
        )
        validators = [IcxValidator(**validator) for validator in result["preps"]]
        return validators

    @classmethod
    async def call(
        cls,
        to_address: str,
        method: str,
        params: dict = {},
        block_number: int = 0,
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
                },
            },
        }
        # Add height param to payload if height is provided.
        if block_number != 0:
            payload["params"]["height"] = Utils.int_to_hex(block_number)

        result = await cls._make_api_request(payload)
        return result

    @classmethod
    async def get_node_status(cls, hostname: str) -> bool:
        async def _make_request(hostname: str) -> int:
            # Make request to ICON node.
            async with httpx.AsyncClient() as client:
                url = f"http://{hostname}:9000/admin/chain"
                print(url)
                r = await client.get(url)
            # Decode node status.
            data = r.json()
            node_status = data[0]
            if node_status.get("state") != "started":
                raise OfflineNodeException
            else:
                return node_status["height"]

        check_count = 3
        node_status_checks = []

        for _ in range(check_count):
            node_status = await _make_request(hostname)
            node_status_checks.append(node_status)
            await asyncio.sleep(2)

        if len(set(node_status_checks)) != 1:
            return True
        else:
            return False

    @classmethod
    async def _make_api_request(cls, payload):
        async with httpx.AsyncClient() as client:
            r = await client.post(f"{cls.ICON_API_ENDPOINT}/api/v3", json=payload)

        if r.status_code == 200:
            data = r.json()
            return data["result"]
        else:
            raise FailedIcxCallException
