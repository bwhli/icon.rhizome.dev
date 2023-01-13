from starlite import Controller, get

from icon_rhizome_dev.constants import API_PREFIX
from icon_rhizome_dev.icx import Icx
from icon_rhizome_dev.models.governance import Validator
from icon_rhizome_dev.tracker import Tracker


class GovernanceController(Controller):
    """
    A controller for routes relating to ICON governance.
    """

    path = f"{API_PREFIX}/governance"

    @get(path="/validators/")
    async def get_validators(self) -> list[Validator]:
        """
        Returns information about all ICON validators.
        """
        validators = Icx.get_validators()
        return validators
