from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from .models import NewsUser
from .forms import NewsUserChangeForm, NewsUserCreationForm


class NewsUserAdmin(auth_admin.UserAdmin):
    # The forms to add and change user instances
    form = NewsUserChangeForm
    add_form = NewsUserCreationForm
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'is_superuser', 'is_staff')
    list_filter = ('is_superuser', 'is_staff')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_superuser', 'is_staff'), }),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(NewsUser, NewsUserAdmin)


