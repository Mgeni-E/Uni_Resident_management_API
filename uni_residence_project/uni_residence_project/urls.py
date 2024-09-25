from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from resident_api.views import (
    BuildingViewSet,
    CustomAuthToken,
    RoomViewSet,
    ResidentViewSet,
)
from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from resident_api.views import home

schema_view = get_schema_view(
    openapi.Info(
        title="University Residence Management API",
        default_version="v1",
        description="API for managing university residence buildings, rooms, and residents",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
router = DefaultRouter()
router.register(r"buildings", BuildingViewSet)
router.register(r"rooms", RoomViewSet)
router.register(r"residents", ResidentViewSet)

urlpatterns = [
    path("", home, name="home"),
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path(
        "docs/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("api-token-auth/", CustomAuthToken.as_view()),
]
