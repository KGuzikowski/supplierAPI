from django.conf import settings
from django.contrib import admin
from django.urls import include, path

from supplierapi.apps.user.urls import router as user_router
from supplierapi.apps.user.views import CustomAuthToken

urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    path("users/", include(user_router.urls)),
    path("authenticate/", CustomAuthToken.as_view()),
]


if settings.DEBUG and "debug_toolbar" in settings.INSTALLED_APPS:
    import debug_toolbar

    urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
