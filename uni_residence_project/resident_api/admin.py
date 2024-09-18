from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Building, Room, Resident

admin.site.register(Building)
admin.site.register(Room)
admin.site.register(Resident)
