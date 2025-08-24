from django.urls import re_path
from .consumers import chat_consumers, online_consumers, tablero_consumers

websocket_urlpatterns = [
    re_path(r"ws/chat/$", chat_consumers.ChatConsumer.as_asgi()),
    re_path(r"ws/online-status/$", online_consumers.OnlineStatusConsumer.as_asgi()),
    re_path(r"ws/tableros/$", tablero_consumers.TableroConsumer.as_asgi()),

]
