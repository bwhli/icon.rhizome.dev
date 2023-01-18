import asyncio
import hashlib
from functools import lru_cache
from pathlib import Path
from random import randint
from typing import Any

from htmlmin.minify import html_minify
from rich import inspect
from starlette.responses import HTMLResponse
from starlite import (
    Controller,
    MediaType,
    Parameter,
    Request,
    Response,
    Template,
    WebSocket,
    WebsocketRouteHandler,
    post,
    websocket,
)
from starlite.datastructures import ResponseHeader
from starlite.exceptions import WebSocketDisconnect

from icon_rhizome_dev import ENV
from icon_rhizome_dev.constants import BLOCK_TIME, EXA, PROJECT_DIR
from icon_rhizome_dev.http_client import HttpClient
from icon_rhizome_dev.icx_async import IcxAsync
from icon_rhizome_dev.models.icx import IcxValidatorIdentity
from icon_rhizome_dev.tracker import Tracker


class AblyPublishController(Controller):

    path = "/ably"

    ABLY_API_KEY = ENV.get("ABLY_PUBLISH_KEY")

    @post(path="/publish/")
    async def publish(self, message: str) -> None:
        r = HttpClient.post()
