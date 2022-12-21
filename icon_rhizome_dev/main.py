from starlite import CacheConfig, Starlite
from starlite.cache.redis_cache_backend import (
    RedisCacheBackend,
    RedisCacheBackendConfig,
)

from icon_rhizome_dev import ENV
from icon_rhizome_dev.controllers.api.address import ApiAddressController
from icon_rhizome_dev.controllers.api.governance import ApiGovernanceController
from icon_rhizome_dev.controllers.api.transaction import ApiTransactionController
from icon_rhizome_dev.controllers.app.governance import AppGovernanceController

# Configure Redis cache settings.
redis_config = RedisCacheBackendConfig(
    url=ENV["REDIS_DB_URL"],
    port=int(ENV["REDIS_DB_PORT"]),
    db=int(ENV["REDIS_DB"]),
)
redis_backend = RedisCacheBackend(config=redis_config)
cache_config = CacheConfig(backend=redis_backend)

# Initialize Starlite app.
app = Starlite(
    route_handlers=[
        ApiAddressController,
        ApiGovernanceController,
        ApiTransactionController,
        AppGovernanceController,
    ],
    cache_config=cache_config,
)
