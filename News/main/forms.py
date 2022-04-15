from django.forms import forms
from .models import *


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('user', 'article', 'text')


class CommentEditForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('user', 'article', 'text')
        widgets = {
            'text': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Text', 'disabled': False, }),
            'user': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'User', 'disabled': False, }),
            'article': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Article', 'disabled': False, }),
        }


class CommentDeleteForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = '__all__'

        widgets = {
            'text': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Text', 'disabled': True,}),
            'user': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'User', 'disabled': True,}),
            'article': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Article', 'disabled': True,}),
        }




class ArticleDeleteForm(forms.Form):
    pass
