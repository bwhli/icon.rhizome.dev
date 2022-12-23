from starlite import Controller, get

from icon_rhizome_dev.constants import API_PREFIX


class AppAddressController(Controller):
    """
    A controller for routes relating to ICON governance.
    """

    path = f"{API_PREFIX}/addresses"
