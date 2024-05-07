from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r"game/(?P<room_code>\w+)/$", consumers.RoomConsumer.as_asgi()),
]