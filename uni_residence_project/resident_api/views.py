from rest_framework import viewsets
from .models import Building, Room, Resident
from .serializers import BuildingSerializer, RoomSerializer, ResidentSerializer

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class BuildingViewSet(viewsets.ModelViewSet):
    queryset = Building.objects.all()
    serializer_class = BuildingSerializer
    permission_classes = [IsAuthenticated]
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


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated]
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


class ResidentViewSet(viewsets.ModelViewSet):
    queryset = Resident.objects.all()
    serializer_class = ResidentSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
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
