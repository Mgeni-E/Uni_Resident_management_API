from django.db import models


class Building(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()


class Room(models.Model):
    building = models.ForeignKey(Building, on_delete=models.CASCADE)
    room_number = models.CharField(max_length=10)
    capacity = models.IntegerField()


class Resident(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True)
    check_in_date = models.DateField()
    check_out_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
