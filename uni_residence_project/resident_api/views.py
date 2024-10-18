from rest_framework import viewsets
from .models import Building, Room, Resident
from .serializers import BuildingSerializer, RoomSerializer, ResidentSerializer

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from rest_framework.authentication import TokenAuthentication, SessionAuthentication

from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope

from rest_framework.views import exception_handler
import logging

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        response.data["status_code"] = response.status_code
        logger.error(f"Error: {exc}, Status Code: {response.status_code}")

    return response


class BuildingViewSet(viewsets.ModelViewSet):
    queryset = Building.objects.all()
    serializer_class = BuildingSerializer
    authentication_classes = [
        OAuth2Authentication,
        TokenAuthentication,
        SessionAuthentication,
    ]
    permission_classes = [
        IsAuthenticated,
        IsAdminUser,
    ]  # Allow access to authenticated users
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["name", "address"]
    search_fields = ["name", "address"]
    ordering_fields = ["name"]

    @method_decorator(cache_page(60 * 15))  # Cache for 15 minutes
    @method_decorator(vary_on_cookie)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "name",
                openapi.IN_QUERY,
                description="Filter by building name",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "address",
                openapi.IN_QUERY,
                description="Filter by building address",
                type=openapi.TYPE_STRING,
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        try:
            return super().list(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Error in BuildingViewSet.list: {str(e)}")
            return Response({"error": "An unexpected error occurred"}, status=500)


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    authentication_classes = [
        OAuth2Authentication,
        TokenAuthentication,
        SessionAuthentication,
    ]
    permission_classes = [
        IsAuthenticated,
        IsAdminUser,
    ]  # Allow access to authenticated users
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["building", "room_number", "capacity"]
    search_fields = ["room_number"]
    ordering_fields = ["capacity"]

    @method_decorator(cache_page(60 * 15))
    @method_decorator(vary_on_cookie)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "building",
                openapi.IN_QUERY,
                description="Filter by building ID",
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                "capacity",
                openapi.IN_QUERY,
                description="Filter by room capacity",
                type=openapi.TYPE_INTEGER,
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        try:
            return super().list(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Error in BuildingViewSet.list: {str(e)}")
            return Response({"error": "An unexpected error occurred"}, status=500)


class ResidentViewSet(viewsets.ModelViewSet):
    queryset = Resident.objects.all()
    serializer_class = ResidentSerializer
    authentication_classes = [
        OAuth2Authentication,
        TokenAuthentication,
        SessionAuthentication,
    ]
    permission_classes = [
        IsAuthenticated,
        IsAdminUser,
    ]  # Allow access to authenticated users
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["room", "check_in_date", "check_out_date"]
    search_fields = ["first_name", "last_name", "email"]
    ordering_fields = ["last_name", "check_in_date"]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "room",
                openapi.IN_QUERY,
                description="Filter by room ID",
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                "check_in_date",
                openapi.IN_QUERY,
                description="Filter by check-in date",
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_DATE,
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        try:
            return super().list(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Error in BuildingViewSet.list: {str(e)}")
            return Response({"error": "An unexpected error occurred"}, status=500)


from django.http import HttpResponse


def home(request):
    return HttpResponse("Welcome to the Uni Residence Management API")


# This class handles custom authentication token generation.
class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "user_id": user.pk, "email": user.email})
