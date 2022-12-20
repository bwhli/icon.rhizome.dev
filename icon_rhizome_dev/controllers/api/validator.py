from starlite import Controller, get

from icon_rhizome_dev.constants import API_PREFIX
from icon_rhizome_dev.models.transaction import Transaction
from icon_rhizome_dev.tracker import Tracker


class ApiValidatorController(Controller):
    """
    A controller for routes relating to ICON validators.
    """

    path = f"{API_PREFIX}/validators/"

    @get(path="/{address:str}/")
    async def get_validator(self, address: str):
        """
        Returns information about an ICON validator.

        Args:
            address: The ICX address of an ICON validator.
        """
        return

    @get(path="/")
    async def get_validators(self):
        """
        Returns information about all ICON validators.
        """
        return
