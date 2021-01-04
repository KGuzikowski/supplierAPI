from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter, SimpleRouter

from supplierapi.apps.company.views import CompanyViewSet
from supplierapi.apps.general.views import (
    CountryViewSet,
    DialingCodeViewSet,
    IndustryViewSet,
)
from supplierapi.apps.user.views import CustomAuthToken, UserViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register("companies", CompanyViewSet)
router.register("industries", IndustryViewSet)
router.register("countries", CountryViewSet)
router.register("dialing_codes", DialingCodeViewSet)

urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    path("", include(router.urls)),
    path("authenticate/", CustomAuthToken.as_view()),
]

if settings.DEBUG and "debug_toolbar" in settings.INSTALLED_APPS:
    import debug_toolbar

    urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
