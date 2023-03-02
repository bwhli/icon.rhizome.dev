from starlite import Controller

from icon_rhizome_dev.constants import API_PREFIX


class CpsController(Controller):
    """
    A controller for routes relating to ICX transactions.
    """

    path = f"{API_PREFIX}/cps"
