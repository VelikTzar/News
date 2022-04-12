from django.urls import path
from .views import *


urlpatterns = [
    path('login/', NewsUserLoginView.as_view(), name="login"),
    path('register/', NewsUserRegisterView.as_view(), name="register"),
    path('logout/', NewsUserLogoutView.as_view(), name="logout")
]
