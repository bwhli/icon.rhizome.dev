from starlite import Controller

from icon_rhizome_dev.constants import API_PREFIX


class ContractsController(Controller):
    """
    A controller for routes relating to ICON smart contracts.
    """

    path = f"{API_PREFIX}/contracts"
