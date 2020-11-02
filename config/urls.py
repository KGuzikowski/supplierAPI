from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter, SimpleRouter

from supplierapi.apps.myAuth.urls import urlpatterns as auth_routes

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

# router.register()

urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    path("api/", include(router.urls)),
    path("auth/", include(auth_routes)),
] + static(settings.MEDIA_URL)


if settings.DEBUG and "debug_toolbar" in settings.INSTALLED_APPS:
    import debug_toolbar

    urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
