import asyncio
import hashlib
from pathlib import Path

import httpx
import orjson
from starlite import Controller, Parameter, Request, Template, get

from icon_rhizome_dev.constants import BLOCK_TIME, EXA, PROJECT_DIR
from icon_rhizome_dev.icx_async import IcxAsync
from icon_rhizome_dev.models.governance import Validator
from icon_rhizome_dev.tracker import Tracker


class GovernanceController(Controller):
    """
    A controller for routes relating to ICON governance.
    """

    path = "/governance"

    @get(path="/")
    async def get_governance(self, block_number: int = 0) -> Template:
        """
        Returns information about all ICON validators.
        """
        return Template(
            name="governance/index.html",
            context={
                "title": "Governance",
                "block_number": block_number,
            },
        )

    @get(path="/htmx/validators/", cache=BLOCK_TIME)
    async def get_htmx_validators(
        self,
        block_number: int = 0,
        sort_by: str = None,
        sort_dir: str = "asc",
        column: str = None,
    ) -> Template:

        # Convert string None to "None None".
        column = None if column == "None" else column
        sort_by = None if sort_by == "None" else sort_by

        # If block number is negative, get current block and substract absolute value of "block_number" from it.
        if block_number < 0:
            last_block_number = await IcxAsync.get_last_block(height_only=True)
            block_number = last_block_number - abs(block_number)

        network_info, icx_usd_price, validators, cps_validators = await asyncio.gather(
            IcxAsync.get_network_info(block_number=block_number),
            IcxAsync.get_icx_usd_price(block_number=block_number),
            IcxAsync.get_validators(block_number=block_number),
            IcxAsync.get_cps_validator_addresses(block_number=block_number),
        )

        total_power = network_info["totalPower"] / EXA
        i_global = network_info["rewardFund"]["Iglobal"] / EXA
        i_prep = network_info["rewardFund"]["Iprep"] / 100

        # Calculate daily/monthly rewards for validators.
        for validator in validators:
            monthly_reward = (validator.power / total_power) * (i_global * i_prep)
            monthly_reward_usd = monthly_reward * icx_usd_price
            daily_reward = (monthly_reward * 12) / 365
            daily_reward_usd = daily_reward * icx_usd_price
            validator.reward_monthly = monthly_reward
            validator.reward_monthly_usd = monthly_reward_usd
            validator.reward_daily = daily_reward
            validator.reward_daily_usd = daily_reward_usd

            if validator.address in cps_validators:
                validator.cps = True

        # Sort validators by key.
        if sort_by is not None:
            validators = sorted(
                validators,
                key=lambda x: getattr(x, sort_by),
                reverse=True if sort_dir == "desc" else False,
            )

        # Get a list of validator images that are in the repo.
        validator_images = [
            image.name
            for image in Path(f"{PROJECT_DIR}/static/images/validators").glob("*.png")
        ]

        # Build template context.
        context = {
            "block_number": block_number,
            "validators": validators,
            "icx_usd_price": icx_usd_price,
            "validator_images": validator_images,
            "sort_by": sort_by,
            "sort_dir": sort_dir,
        }

        # Only return column if column is specified.
        if column is not None:
            return Template(
                name=f"governance/htmx/validators_column_{column}.html",
                context=context,
            )

        return Template(
            name="governance/htmx/validators.html",
            context=context,
        )

    @get(path="/htmx/node-status-check-modal/")
    async def get_htmx_node_status_check_modal(
        self,
        address: str,
        hostname: str = None,
    ) -> Template:

        if hostname is None:
            api_endpoint = await Tracker.get_api_endpoint(address)
            hostname = api_endpoint.replace(":9000", "")
            hostname = hostname.replace("http://", "")
            hostname = hostname.replace("https://", "")

        return Template(
            name="governance/htmx/node_status_check_modal.html",
            context={"address": address, "hostname": hostname},
        )

    @get(path="/htmx/node-status-check-result/")
    async def get_htmx_node_status_check(
        self,
        hostname: str = None,
    ) -> Template:
        node_status = await IcxAsync.get_node_status(hostname)
        return Template(
            name="governance/htmx/node_status_check_result.html",
            context={"result": node_status},
        )
