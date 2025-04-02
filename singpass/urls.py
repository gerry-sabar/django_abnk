from django.urls import path
from .views import SingpassCallback, SingpassAPI

urlpatterns = [
    path('', SingpassAPI.as_view(), name='singpass-api'),
    path('callback', SingpassCallback.as_view(), name='singpass-callback'),
]