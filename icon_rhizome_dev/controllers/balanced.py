from starlite import Controller, get

from icon_rhizome_dev.constants import API_PREFIX, BLOCK_TIME
from icon_rhizome_dev.tracker import Tracker


class BalancedController(Controller):
    """
    A controller for routes relating to Balanced.
    """

    path = f"{API_PREFIX}/balanced"
