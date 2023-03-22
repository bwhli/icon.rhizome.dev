import asyncio
import io
from datetime import datetime, timezone

import pandas as pd
from pydantic import BaseModel, ValidationError, validator
from rich import print
from starlite import (
    Body,
    Controller,
    RequestEncodingType,
    Template,
    get,
    post,
    status_codes,
)
from starlite.exceptions import HTTPException

from icon_rhizome_dev.balanced import Balanced
from icon_rhizome_dev.balanced.balanced_dex import BalancedDex, BalancedDividendClaim
from icon_rhizome_dev.constants import SM_DISCORD_ADDRESSES
from icon_rhizome_dev.controllers.api.v1 import API_PREFIX
from icon_rhizome_dev.icx import Icx
from icon_rhizome_dev.models.icx import IcxTransaction
from icon_rhizome_dev.s3 import S3
from icon_rhizome_dev.tracker import Tracker
from icon_rhizome_dev.utils import Utils


class Api_ToolsController(Controller):
    """
    A controller for routes relating to ICX transactions.
    """

    path = f"{API_PREFIX}/tools"

    @get(path="/timestamp-to-block/{timestamp:int}/")
    async def convert_timestamp_to_block(
        self,
        timestamp: int,
    ) -> dict[str, int]:
        """
        Returns block height for the provided timestamp.

        Args:
            timestamp (int): Unix timestamp in microseconds.

        Returns:
            dict: A dictionary containing the source timestamp and block number.
        """
        block = await Tracker.get_block_from_timestamp(
            timestamp, block_number_only=True
        )
        return {
            "block": block,
            "timestamp": timestamp,
        }

    @get(path="/calculate-usd-value/")
    async def calculate_usd_value(
        self,
        value: str,  # hexadecimal representation of value
        block_number: int = 0,
    ) -> dict[str, float | int]:
        value_decimal = int(value, 16) / 10**18
        icx_usd_price = await Icx.get_icx_usd_price(block_number)
        return {
            "result": "success",
            "data": {
                "icx_value": value,
                "icx_value_decimal": value_decimal,
                "usd_value": value_decimal * icx_usd_price,
                "block_number": block_number,
            },
        }
