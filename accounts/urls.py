

from django.urls import path

from .views import LoginView, SignUpView

from . import views


urlpatterns = [
    path("",  views.index, name="account"),
    path("signup/", views.register, name="signup"),
    path("login/", LoginView.as_view(), name="login"),
]