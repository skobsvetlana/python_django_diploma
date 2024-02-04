from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm
from django.forms import ModelForm, ImageField
from django.contrib.auth.models import User

from django import forms


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = "user", "username", "password"