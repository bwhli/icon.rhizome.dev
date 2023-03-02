import asyncio

from starlite import Controller, WebSocket, WebsocketRouteHandler
from starlite.exceptions import WebSocketDisconnect

from icon_rhizome_dev.icx_async import IcxAsync
from icon_rhizome_dev.utils import Utils


class WebSocketController(Controller):

    path = "/ws"

    @WebsocketRouteHandler(path="/")
    async def websocket_handler(
        self,
        socket: WebSocket,
        channel: str = None,
    ) -> None:
        await socket.accept()

        current_block = await IcxAsync.get_last_block(height_only=True)

        while True:
            try:
                (
                    stale_block,
                    current_block,
                ) = current_block, await IcxAsync.get_last_block(height_only=True)
                if current_block != stale_block:
                    data = f'<span id="block-height" hx-swap-oob="innerHTML">{Utils.format_number(current_block)}</span>'
                    await socket.send_text(data)

                await asyncio.sleep(0.5)

            except WebSocketDisconnect:
                await socket.close()
                return
