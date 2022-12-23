import os

from jinja2 import Environment, FileSystemLoader
from starlite import CacheConfig, Request, Starlite, Template, TemplateConfig, get
from starlite.cache.redis_cache_backend import (
    RedisCacheBackend,
    RedisCacheBackendConfig,
)
from starlite.template.jinja import JinjaTemplateEngine

from icon_rhizome_dev import ENV
from icon_rhizome_dev.controllers.api.address import ApiAddressController
from icon_rhizome_dev.controllers.api.governance import ApiGovernanceController
from icon_rhizome_dev.controllers.api.transaction import ApiTransactionController
from icon_rhizome_dev.controllers.app.governance import AppGovernanceController
from icon_rhizome_dev.icx import Icx
from icon_rhizome_dev.utils import Utils

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
        ApiAddressController,
        ApiGovernanceController,
        ApiTransactionController,
        AppGovernanceController,
        home_handler,
    ],
    cache_config=cache_config,
    template_config=TemplateConfig(
        directory=f"{os.path.dirname(__file__)}/templates",
        engine=JinjaTemplateEngine,
    ),
)
