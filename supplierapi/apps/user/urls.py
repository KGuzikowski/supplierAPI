from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from .views import UserViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("", UserViewSet)
