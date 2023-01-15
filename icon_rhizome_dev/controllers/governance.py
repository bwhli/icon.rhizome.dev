import asyncio
import hashlib
from pathlib import Path

import orjson
from starlite import Controller, Request, Template, get

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
    async def get_governance(self) -> Template:
        """
        Returns information about all ICON validators.
        """
        return Template(
            name="governance/index.html",
            context={},
        )

    @get(path="/htmx/validators/", cache=BLOCK_TIME)
    async def get_htmx_validators(self, request: Request) -> Template:

        network_info, icx_usd_price, validators, cps_validators = await asyncio.gather(
            IcxAsync.get_network_info(),
            IcxAsync.get_icx_usd_price(),
            IcxAsync.get_validators(),
            IcxAsync.get_cps_validator_addresses(),
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

        validator_images = [
            image.name
            for image in Path(f"{PROJECT_DIR}/static/images/validators").glob("*.png")
        ]

        return Template(
            name="governance/htmx/validators.html",
            context={
                "validators": validators,
                "icx_usd_price": icx_usd_price,
                "validator_images": validator_images,
            },
        )
