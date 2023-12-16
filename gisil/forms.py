from django import forms
from .models import GisilValues

class GisilForm(forms.ModelForm):
    class Meta:
        model = GisilValues
        fields = "__all__"