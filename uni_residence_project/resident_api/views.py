from rest_framework import viewsets
from .models import Building, Room, Resident
from .serializers import BuildingSerializer, RoomSerializer, ResidentSerializer


class BuildingViewSet(viewsets.ModelViewSet):
    queryset = Building.objects.all()
    serializer_class = BuildingSerializer


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class ResidentViewSet(viewsets.ModelViewSet):
    queryset = Resident.objects.all()
    serializer_class = ResidentSerializer


from django.http import HttpResponse


def home(request):
    return HttpResponse("Welcome to the Uni Residence Management API")
