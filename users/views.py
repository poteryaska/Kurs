from django.shortcuts import render
from django.contrib.auth.views import LoginView as BaseLoginView, PasswordResetDoneView
class LoginView(BaseLoginView):
    template_name = 'users/login.html'