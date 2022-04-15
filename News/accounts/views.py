from django.contrib.auth import views as auth_views, login
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import *


class NewsUserLoginView(auth_views.LoginView):
    template_name = "accounts/login.html"
    success_url = reverse_lazy("index")


class NewsUserLogoutView(auth_views.LogoutView):
    template_name = "accounts/logout.html"
    next_page = reverse_lazy("login")


class NewsUserRegisterView(CreateView):
    form_class = NewsUserCreationForm
    template_name = "accounts/register.html"
    success_url = reverse_lazy("index")

    def form_valid(self, form):
        result = super().form_valid(form)
        login(self.request, self.object, backend='django.contrib.auth.backends.ModelBackend')
        return result


