import asyncio
import hashlib
from functools import lru_cache
from pathlib import Path
from random import randint
from typing import Any

from htmlmin.minify import html_minify
from rich import inspect
from starlette.responses import HTMLResponse
from starlite import Controller, WebSocket, WebsocketRouteHandler, get
from starlite.datastructures import ResponseHeader
from starlite.exceptions import WebSocketDisconnect

from icon_rhizome_dev.constants import BLOCK_TIME, EXA, PROJECT_DIR
from icon_rhizome_dev.icx_async import IcxAsync
from icon_rhizome_dev.models.icx import IcxValidatorIdentity
from icon_rhizome_dev.tracker import Tracker
from icon_rhizome_dev.utils import Utils


class WebSocketController(Controller):

    path = "/ws"

    @WebsocketRouteHandler(path="/")
    async def websocket_handler(self, socket: WebSocket) -> None:
        await socket.accept()

        current_block = await IcxAsync.get_last_block(height_only=True)

        while True:
            try:

                stale_block, current_block = current_block, await IcxAsync.get_last_block(height_only=True)  # fmt: skip

                if current_block != stale_block:
                    data = f'<span id="block-height" hx-swap-oob="innerHTML">{Utils.format_number(current_block)}</span>'  # fmt: skip
                    await socket.send_text(data)

                await asyncio.sleep(0.5)

            except WebSocketDisconnect as e:
                await socket.close()
                return
