from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.

class Patient(models.Model):
    first_name = models.CharField(max_length=50)
    second_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone_number = PhoneNumberField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Dr:{self.first_name} {self.second_name}"
    