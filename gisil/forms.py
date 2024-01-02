from django import forms
from .models import GisilValues
from django.contrib.auth.models import User

class GisilForm(forms.ModelForm):
    class Meta:
        model = GisilValues
        fields = "__all__"

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "password"]