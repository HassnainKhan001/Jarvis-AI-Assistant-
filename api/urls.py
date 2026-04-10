from django.urls import path
from .views import assistant_api, toggle_listener

urlpatterns = [
    path('ask', assistant_api, name='assistant_api'),
    path('listener/toggle', toggle_listener, name='toggle_listener'),
]
