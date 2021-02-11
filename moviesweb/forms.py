"""Django model describes the logical structure of an object, its behavior, and the way its parts
are represented to us, a Form class describes a form and determines how it works and appears."""
from typing import Tuple, Type

from django import forms
from django.contrib.auth.forms import UserCreationForm
import django.contrib.auth.models

from django.forms.fields import EmailField


class SignUpForm(UserCreationForm):
    """Forms for user registration"""
    email: EmailField = forms.EmailField(max_length=254, required=False,
                                         help_text=
                                         'Optional. If you give us valid email, we will be able if '
                                         'you want to send you the detailed content you need ')

    class Meta:
        model: Type = django.contrib.auth.models.User
        fields: Tuple[str, str, str, str] = ('username', 'email', 'password1', 'password2',)
