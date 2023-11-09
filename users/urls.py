from django.urls import path

from users.apps import UsersConfig
from users.views import LoginView, LogoutView, RegisterView, UserConfirmationSentView, UserConfirmEmailView, \
    UserConfirmedView, UserUpdateView, UserResetView, UserResetDoneView, UserResetConfirmView, \
    UserResetCompleteView

app_name = UsersConfig.name

urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('email_confirmation_sent/', UserConfirmationSentView.as_view(), name='email_confirmation_sent'),
    path('confirm_email/<str:uidb64>/<str:token>/', UserConfirmEmailView.as_view(), name='confirm_email'),
    path('email_confirmed/', UserConfirmedView.as_view(), name='email_confirmed'),
    path("profile/", UserUpdateView.as_view(), name="profile"),
    path('password_reset/', UserResetView.as_view(), name='password_reset'),
    path('password_reset/done/', UserResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset/<uidb64>/<token>/', UserResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset/complete/', UserResetCompleteView.as_view(), name='password_reset_complete')


    ]