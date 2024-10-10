from django.db import models

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from cryptography.fernet import Fernet


def encrypt_data(data):
    key = Fernet.generate_key()
    f = Fernet(key)
    return f.encrypt(data.encode()).decode(), key.decode()


def decrypt_data(encrypted_data, key):
    f = Fernet(key.encode())
    return f.decrypt(encrypted_data.encode()).decode()


class EncryptedCharField(models.CharField):
    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        return decrypt_data(value, self.key)

    def to_python(self, value):
        if isinstance(value, str):
            return value
        if value is None:
            return value
        return decrypt_data(value, self.key)

    def get_prep_value(self, value):
        value, self.key = encrypt_data(value)
        return value


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

    def clean(self):
        if self.check_out_date and self.check_out_date < self.check_in_date:
            raise ValidationError(_("Check-out date must be after check-in date."))

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
