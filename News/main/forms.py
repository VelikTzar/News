import django.forms as forms
from .models import *


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text', )


class CommentEditForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text', )
        widgets = {
            'text': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Text', 'disabled': False, }),
        }


class CommentDeleteForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)

        widgets = {
            'text': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Text', 'disabled': True,}),
        }


