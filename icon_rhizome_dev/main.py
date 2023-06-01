from starlite import Starlite, StaticFilesConfig, TemplateConfig
from starlite.config import CompressionConfig
from starlite.contrib.jinja import JinjaTemplateEngine

from icon_rhizome_dev.constants import BLOCK_TIME, NOW, PROJECT_DIR, YEAR
from icon_rhizome_dev.controllers.governance import GovernanceController
from icon_rhizome_dev.utils import Utils

template_config = TemplateConfig(
    directory=f"{PROJECT_DIR}/templates",
    engine=JinjaTemplateEngine,
)

# Global template variables.
template_config.engine_instance.engine.globals["BLOCK_TIME"] = BLOCK_TIME
template_config.engine_instance.engine.globals["BLOCKS_1D"] = 172800
template_config.engine_instance.engine.globals["NOW"] = int(NOW.timestamp())
template_config.engine_instance.engine.globals["YEAR"] = YEAR

# Global template functions.
template_config.engine_instance.engine.globals["format_asset_amount"] = Utils.format_asset_amount  # fmt: skip
template_config.engine_instance.engine.globals["format_asset_symbol"] = Utils.format_asset_symbol  # fmt: skip
template_config.engine_instance.engine.globals["format_number"] = Utils.format_number  # fmt: skip
template_config.engine_instance.engine.globals["format_percentage"] = Utils.format_percentage  # fmt: skip
template_config.engine_instance.engine.globals["get_validator_name_from_address"] = Utils.get_validator_name_from_address  # fmt: skip


# Initialize Starlite app.
app = Starlite(
    compression_config=CompressionConfig(
        backend="brotli",
        brotli_gzip_fallback=True,
    ),
    route_handlers=[
        GovernanceController,
    ],
    static_files_config=[
        StaticFilesConfig(directories=[f"{PROJECT_DIR}/static"], path="/static"),
    ],
    template_config=template_config,
)
