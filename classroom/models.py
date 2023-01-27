from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.html import escape, mark_safe


class User(AbstractUser):
    is_admin = models.BooleanField(default=False)
    is_cashier = models.BooleanField(default=False)

    class Meta:
        swappable = 'AUTH_USER_MODEL'


class Customer(models.Model):
    id=models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=10,
    help_text='Maximum of 10 digits')
    email_add = models.CharField(max_length=100, blank=True)
    car_model = models.CharField(max_length=100)
    car_color = models.CharField(max_length=100)
    license_plate = models.CharField(max_length=100)
    comment = models.TextField(max_length=5000, blank=True)
    is_payed = models.BooleanField(default=False)
    hours_spent = models.CharField(null=True, blank=True, max_length=1000)
    total_cost = models.IntegerField(null=True, blank=True)
    register_name = models.CharField(max_length=100)
    card_number = models.CharField(max_length=1000)
    reg_date = models.DateTimeField(auto_now_add=True, null=True)
    parking_space = models.CharField(max_length=100, null=True)
    parking_time = models.DateTimeField(null=True, blank= True)
    exit_time = models.DateTimeField(null=True, blank=True)
    def clean_license_plate (self):
        plate = self.cleaned_data.get("license_plate")
        if plate == "":
            raise ValidationError('This field cannot be left blank')
        return plate
        for instance in Customer.objects.all():
            if instance.license_plate == plate:
                raise ValidationError (license_plate + ' is already exist in the system.')
        return plate