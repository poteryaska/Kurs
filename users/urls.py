from django.urls import path

from users.apps import UsersConfig
from users.views import LoginView

app_name = UsersConfig.name

urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    ]