"""Django model describes the logical structure of an object, its behavior, and the way its parts
are represented to us, a Form class describes a form and determines how it works and appears."""
from django import forms
from django.contrib.auth.forms import UserCreationForm
import django.contrib.auth.models


class SignUpForm(UserCreationForm):
    """Forms for user registration"""
    email = forms.EmailField(max_length=254, required=False,
                             help_text=
                             'Optional. If you give us valid email, we will be able if you want to'
                             ' send you the detailed content you need ')

    class Meta:
        model = django.contrib.auth.models.User
        fields = ('username', 'email', 'password1', 'password2',)
