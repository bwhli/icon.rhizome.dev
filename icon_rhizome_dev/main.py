from starlite import Starlite

from icon_rhizome_dev.controllers.api.transaction import ApiTransactionController

app = Starlite(route_handlers=[ApiTransactionController])
