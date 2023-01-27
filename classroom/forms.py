from classroom.models import User, Customer
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Customer,User
from bootstrap_modal_forms.forms import BSModalModelForm, BSModalForm
from bootstrap_modal_forms.mixins import PopRequestMixin, CreateUpdateAjaxMixin
from django.contrib.auth import get_user_model
from django.core.signals import setting_changed
from django.dispatch import receiver
from django.core.exceptions import ValidationError


class CustomerForm(BSModalModelForm):
    class Meta:
        model = Customer
        fields = ('first_name', 'last_name', 'license_plate', 'parking_time', 'car_model', 'car_color', 'phone_number', 'comment', 'is_payed')


class UserForm(BSModalModelForm):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')
        def clean_email(self):
            # Get the email
            email = self.cleaned_data.get('email')

            # Check to see if any users already exist with this email as a username.
            try:
                match = User.objects.get(email=email)
            except Exception as e:
                # Unable to find a user, this is fine
                return email

            # A user was found with this as a username, raise an error.
            raise forms.ValidationError('This email address is already in use.')
