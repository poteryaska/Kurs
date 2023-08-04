from django.shortcuts import render
from django.urls import path

from mailing.views import MainView, MessageCreate, MessagesView, MessageCard, MessageUpdate, MessageDelete, ClientView, \
    ClientCard, ClientUpdate, ClientDelete, ClientCreate

app_name = "mailing"

urlpatterns = [
    path("", MainView.as_view(), name="main_page"),
    path("messages/", MessagesView.as_view(), name="messages"),
    path("create/", MessageCreate.as_view(), name="message_create"),
    path("message_delete/<slug:message_slug>", MessageDelete.as_view(), name="message_delete"),
    path("message_update/<slug:message_slug>", MessageUpdate.as_view(), name="message_update"),
    path("message_card/<slug:message_slug>", MessageCard.as_view(), name="message_card"),
    path("clients/", ClientView.as_view(), name="clients"),
    path("client_create/", ClientCreate.as_view(), name="client_create"),
    path("client_delete/<slug:client_slug>", ClientDelete.as_view(), name="client_delete"),
    path("client_update/<slug:client_slug>", ClientUpdate.as_view(), name="client_update"),
    path("client_card/<slug:client_slug>", ClientCard.as_view(), name="client_card"),
    ]