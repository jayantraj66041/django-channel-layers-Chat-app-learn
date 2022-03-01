from django.urls import path
from app.consumers import MySyncConsumer, MyAsyncConsumer

ws_urlpatterns = [
    path("ws/mysc/", MySyncConsumer.as_asgi()),
    path("ws/myasc/", MyAsyncConsumer.as_asgi()),
]