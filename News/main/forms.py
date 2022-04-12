from django.forms import forms
from .models import *


class ProfileForm(forms.Form):
    class Meta:
        model = Profile
        fields = '__all__'


