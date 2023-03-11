import asyncio
from pathlib import Path

from starlite import Controller, Template, get

from icon_rhizome_dev.constants import EXA, PROJECT_DIR
from icon_rhizome_dev.icx import Icx
from icon_rhizome_dev.models.icx import IcxValidator
from icon_rhizome_dev.tracker import Tracker


class GovernanceController(Controller):
    """
    A controller for routes relating to ICON governance.
    """

    path = "/governance"

    async def process_block_number(
        self,
        block_number: int = 0,
    ) -> int:
        # Historical querying is not supported before this block.
        MIN_BLOCK_NUMBER = 43_550_000

        # If block number is negative, get current block and substract absolute value of "block_number" from it.
        if block_number < 0:
            last_block_number = await Icx.get_last_block(height_only=True)
            block_number = last_block_number - abs(block_number)

        if block_number < MIN_BLOCK_NUMBER:
            last_block_number = await Icx.get_last_block(height_only=True)
            block_number = last_block_number

        return block_number

    async def get_validators(
        self,
        block_number: int = 0,
    ) -> list[IcxValidator]:
        """
        Returns a list of ICON validators.

        Args:
            block_number: The block height to query.
        """
        block_number = await self.process_block_number(block_number)

        network_info, icx_usd_price, validators, cps_validators = await asyncio.gather(
            Icx.get_network_info(block_number=block_number),
            Icx.get_icx_usd_price(block_number=block_number),
            Icx.get_validators(block_number=block_number),
            Icx.get_cps_validator_addresses(block_number=block_number),
        )

        total_power = network_info["totalPower"] / EXA
        i_global = network_info["rewardFund"]["Iglobal"] / EXA
        i_prep = network_info["rewardFund"]["Iprep"] / 100

        # Calculate daily/monthly rewards for validators.
        for index, validator in enumerate(validators, start=1):
            validator.rank = index
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

        return validators

    def get_validator_images(self) -> list[str]:
        """
        Returns a list of paths for validator images that exist.
        """
        validator_images = [
            image.name
            for image in Path(f"{PROJECT_DIR}/static/images/validators").glob("*.png")
        ]
        return validator_images

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

    ###############
    # HTMX Routes #
    ###############

    @get(path="/htmx/overview/")
    async def get_governance_htmx_overview(
        self,
        block_number: int = 0,
    ) -> Template:
        block_number = await self.process_block_number(block_number)
        network_info = await Icx.get_network_info(block_number)
        return Template(
            name="governance/htmx/overview.html",
            context={
                "block_number": block_number,
                "network_info": network_info,
            },
        )

    @get(path="/htmx/validators/column/{column:str}/")
    async def get_htmx_validators_column(
        self,
        column: str,
        block_number: int = 0,
    ) -> Template:

        # Convert string None to "None None".
        column = None if column == "None" else column

        # Fetch validator info.
        validators = await self.get_validators(block_number=block_number)
        return Template(
            name=f"governance/htmx/validators_column_{column}.html",
            context={
                "block_number": block_number,
                "validators": validators,
                "validator_images": self.get_validator_images(),
            },
        )

    @get(path="/htmx/validators/rows/")
    async def get_htmx_validators_row(
        self,
        block_number: int = 0,
        sort_by: str | None = None,
        sort_dir: str = "asc",
    ) -> Template:

        # Fetch validator info.
        validators = await self.get_validators(
            block_number=block_number,
        )

        # Only return column if column is specified.
        return Template(
            name="governance/htmx/validators_rows.html",
            context={
                "block_number": block_number,
                "validators": validators,
                "validator_images": self.get_validator_images(),
                "sort_by": sort_by,
                "sort_dir": sort_dir,
                "hx_swap_oob": True,
            },
        )

    @get(path="/htmx/validators/")
    async def get_htmx_validators(
        self,
        block_number: int = 0,
        sort_by: str | None = None,
        sort_dir: str = "asc",
        column: str | None = None,
        rows: str | None = None,
    ) -> Template:

        # Convert string None to "None None".
        column = None if column == "None" else column
        rows = None if rows == "None" else rows
        sort_by = None if sort_by == "None" else sort_by

        # Fetch validator info.
        validators = await self.get_validators(block_number=block_number)

        # Sort validators by key.
        if sort_by is not None:
            validators = sorted(
                validators,
                key=lambda x: getattr(x, sort_by),
                reverse=True if sort_dir == "desc" else False,
            )

        return Template(
            name="governance/htmx/validators.html",
            context={
                "block_number": block_number,
                "validators": validators,
                "validator_images": self.get_validator_images(),
                "sort_by": sort_by,
                "sort_dir": sort_dir,
            },
        )

    @get(path="/htmx/node-status-check-modal/")
    async def get_htmx_node_status_check_modal(
        self,
        address: str,
        hostname: str | None = None,
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
        hostname: str | None = None,
    ) -> Template:
        node_status = await Icx.get_node_status(hostname)
        return Template(
            name="governance/htmx/node_status_check_result.html",
            context={"result": node_status},
        )
