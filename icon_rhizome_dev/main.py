import os

from starlite import CacheConfig, Request, Starlite, Template, TemplateConfig, get
from starlite.cache.redis_cache_backend import (
    RedisCacheBackend,
    RedisCacheBackendConfig,
)
from starlite.contrib.jinja import JinjaTemplateEngine

from icon_rhizome_dev import ENV
from icon_rhizome_dev.controllers.address import AddressController
from icon_rhizome_dev.controllers.governance import GovernanceController
from icon_rhizome_dev.controllers.tools import ToolsController
from icon_rhizome_dev.controllers.transaction import TransactionController
from icon_rhizome_dev.icx import Icx
from icon_rhizome_dev.utils import Utils

PROJECT_DIR = os.path.dirname(__file__)

# Configure Redis cache settings.
redis_config = RedisCacheBackendConfig(
    url=ENV["REDIS_DB_URL"],
    port=int(ENV["REDIS_DB_PORT"]),
    db=int(ENV["REDIS_DB"]),
)
redis_backend = RedisCacheBackend(config=redis_config)
cache_config = CacheConfig(backend=redis_backend)


@get("/", cache=2)
def home_handler(request: Request) -> Template:
    validators = Icx.get_validators()
    return Template(
        name="index.html",
        context={"validators": validators, "fmt": Utils.fmt},
    )


# Initialize Starlite app.
app = Starlite(
    route_handlers=[
        AddressController,
        GovernanceController,
        ToolsController,
        TransactionController,
        home_handler,
    ],
    template_config=TemplateConfig(
        directory=f"{PROJECT_DIR}/templates",
        engine=JinjaTemplateEngine,
    ),
)
