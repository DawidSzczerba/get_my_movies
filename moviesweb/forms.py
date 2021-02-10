from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=False,
                             help_text='Optional. If you give us valid email, we will be able if you want to'
                                       ' send you the detailed content you need ')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2',)
