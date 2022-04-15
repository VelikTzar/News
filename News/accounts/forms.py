from django import forms as forms
from django.contrib.auth.models import Group
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from guardian.shortcuts import assign_perm

from News.main.models import Profile

from .models import NewsUser


class NewsUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = NewsUser
        fields = ('email', )

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        profile = Profile(user=user, email=self.cleaned_data["email"])
        my_group = Group.objects.get(name='Default user')
        if commit:
            user.save()
            profile.save()
            my_group.user_set.add(user)
            assign_perm('change_newsuser', user, user)
            assign_perm('delete_newsuser', user, user)
            assign_perm('view_newsuser', user, user)
            assign_perm('change_profile', user, profile)
            assign_perm('delete_profile', user, profile)
            assign_perm('view_profile', user, profile)

        return user


class NewsUserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = NewsUser
        fields = ('email', 'password', 'is_staff', 'is_superuser')

