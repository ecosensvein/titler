from channels.routing import route
from collector.consumers import ws_connect, ws_message

channel_routing = [
    route("websocket.connect", ws_connect, path=r"^/$"),
    route("websocket.receive", ws_message, path=r"^/$"),
]
