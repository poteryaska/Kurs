from django.shortcuts import render
from django.urls import path

from mailing.views import MainView, MessageCreate, MessagesView

app_name = "mailing"

urlpatterns = [
    path("", MainView.as_view(), name="main_page"),
    path("messages/", MessagesView.as_view(), name="messages"),
    path("create/", MessageCreate.as_view(), name="template"),
    ]