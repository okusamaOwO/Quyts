from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r"game/room/play/(?P<room_code>\w+)/$", consumers.RoomConsumer.as_asgi()),
]