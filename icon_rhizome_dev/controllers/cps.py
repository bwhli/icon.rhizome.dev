from starlite import Controller, get

from icon_rhizome_dev.constants import API_PREFIX, BLOCK_TIME
from icon_rhizome_dev.tracker import Tracker


class CpsController(Controller):
    """
    A controller for routes relating to ICX transactions.
    """

    path = f"{API_PREFIX}/cps"
