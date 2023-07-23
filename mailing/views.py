from django.shortcuts import render
from django.urls import path

from mailing.urls import MainView

app_name = "mailing"

urlpatterns = [
    path("", MainView.as_view(), name="main_page"),
    ]