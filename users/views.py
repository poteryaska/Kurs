from django.contrib.auth import login
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView as BaseLoginView, PasswordResetDoneView, PasswordResetView, \
    PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.urls import reverse_lazy, reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.views.generic import CreateView, TemplateView, UpdateView

import config.settings
from config import settings
from users.forms import UserForm, UserProfileForm
from users.models import User


class LoginView(BaseLoginView):
    template_name = 'users/login.html'

class LogoutView(BaseLogoutView):
    template_name = 'users/login.html'


class RegisterView(CreateView):
    model = User
    form_class = UserForm
    success_url = reverse_lazy('users:login')
    template_name = 'users/register.html'

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        user.save()
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        activation_url = reverse_lazy('users:confirm_email', kwargs={'uidb64': uid, 'token': token})
        current_site = config.settings.SITE_NAME

        send_mail(
                  subject="Registration on Site!",
                  from_email=settings.EMAIL_HOST_USER,
                  message=f"Accept your email address. Go on: http://{current_site}{activation_url}",
                  fail_silently=False,
                  recipient_list=[user.email]
        )

        return redirect('users:email_confirmation_sent')

class UserConfirmationSentView(PasswordResetDoneView):
    template_name = 'users/registration_sent_done.html'

class UserConfirmEmailView(View):
    """User confirms his registration."""

    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64)
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            return redirect('users:email_confirmed')
        else:
            return redirect('users:email_confirmation_failed')

class UserConfirmedView(TemplateView):
    """User registration done and show information about it."""
    template_name = 'users/registration_confirmed.html'
    title = "Your email is activated."

class UserUpdateView(UpdateView):
    model = User
    success_url = reverse_lazy('mailing:main_page')
    form_class = UserProfileForm
    template_name = "users/profile.html"


    def get_object(self, queryset=None):
        return self.request.user

class UserResetView(PasswordResetView):
    """First step for reset user password"""
    template_name = "users/password_reset_form.html"
    email_template_name = "users/password_reset_email.html"
    success_url = reverse_lazy('users:password_reset_done')


class UserResetDoneView(PasswordResetDoneView):
    """Second step for reset user password"""
    template_name = "users/password_reset_done.html"


class UserResetConfirmView(PasswordResetConfirmView):
    """User confirm reset and changed password"""
    template_name = "users/password_reset_confirm.html"
    success_url = reverse_lazy("users:password_reset_complete")


class UserResetCompleteView(PasswordResetCompleteView):
    """Reset done information"""
    template_name = "users/password_reset_complete.html"
