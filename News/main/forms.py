from django.forms import forms
from .models import *


class ProfileForm(forms.Form):
    class Meta:
        model = Profile
        fields = '__all__'


class ProfileDeleteForm(forms.Form):
    pass


class ArticleCreateForm(forms.Form):
    pass


class ArticleEditForm(forms.Form):
    pass


class ArticleDeleteForm(forms.Form):
    pass
