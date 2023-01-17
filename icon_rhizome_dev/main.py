import os
from datetime import datetime

from htmlmin.minify import html_minify
from starlette.responses import HTMLResponse
from starlite import (
    AllowedHostsConfig,
    CacheConfig,
    Request,
    Response,
    Starlite,
    StaticFilesConfig,
    Template,
    TemplateConfig,
    get,
)
from starlite.cache.redis_cache_backend import (
    RedisCacheBackend,
    RedisCacheBackendConfig,
)
from starlite.config import CompressionConfig
from starlite.contrib.jinja import JinjaTemplateEngine

from icon_rhizome_dev import ENV
from icon_rhizome_dev.constants import BLOCK_TIME, PROJECT_DIR
from icon_rhizome_dev.controllers.address import AddressController
from icon_rhizome_dev.controllers.governance import GovernanceController
from icon_rhizome_dev.controllers.tools import ToolsController
from icon_rhizome_dev.controllers.transaction import TransactionController
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

template_config = TemplateConfig(
    directory=f"{PROJECT_DIR}/templates",
    engine=JinjaTemplateEngine,
)
template_config.engine_instance.engine.globals["BLOCK_TIME"] = BLOCK_TIME
template_config.engine_instance.engine.globals["NOW"] = int(datetime.now().timestamp())

template_config.engine_instance.engine.globals["format_number"] = Utils.format_number
template_config.engine_instance.engine.globals["format_percentage"] = Utils.format_percentage  # fmt: skip


@get("/", cache=2)
def home_handler(request: Request) -> Template:
    response = Template(
        name="index.html",
        context={},
    )
    return response


# Initialize Starlite app.
app = Starlite(
    allowed_hosts=AllowedHostsConfig(
        allowed_hosts=[
            "localhost",
            "icon.rhizome.dev",
        ],
    ),
    cache_config=cache_config,
    compression_config=CompressionConfig(backend="brotli", brotli_gzip_fallback=True),
    route_handlers=[
        AddressController,
        GovernanceController,
        ToolsController,
        TransactionController,
        home_handler,
    ],
    static_files_config=[
        StaticFilesConfig(directories=[f"{PROJECT_DIR}/static"], path="/static"),
    ],
    template_config=template_config,
)
