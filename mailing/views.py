from datetime import datetime
from mailbox import Message
from mailing.cron import sendmails

import pytz
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

import config.settings
import mailing.models
from config import settings
from mailing.forms import MessageCreateForm, ClientCreateForm, TransferCreateForm
from mailing.models import Messages, Transfer, Client, Logs


class MainView(LoginRequiredMixin, ListView):
    """Main page with blog and statistic"""
    model = Messages
    template_name = "mailing/messages.html"

    # def get_queryset(self):
    #     """Execute blog part cash on main page"""
    #     if config.settings.CACHE_ENABLED:
    #         key = 'main_blog'
    #         cache_data = cache.get(key)
    #         if cache_data is None:
    #             cache_data = Blog.objects.order_by('?')[:3]
    #             cache.set(key, cache_data)
    #     else:
    #         cache_data = Blog.objects.order_by('?')[:3]
    #     return cache_data

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context["Title"] = "Main"
    #     # show blogs
    #     context["Blog"] = self.get_queryset()
    #     # show statistic
    #     context["all_transmissions"] = len(Transfer.objects.all())
    #     context["active_transmissions"] = len(Transfer.objects.filter(is_published=True))
    #     context["all_clients"] = len(Transfer.objects.all())
    #     context["unique_clients"] = len(Transfer.objects.all().values('email').distinct())
    #     return context

class ClientView(ListView):
    model = Client
    template_name = "mailing/clients.html"

    def get_queryset(self):
        queryset = super().get_queryset().all()
        # if not self.request.user.is_staff:
        #     queryset = super().get_queryset().filter(owner=self.request.user)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["Title"] = "Clients"
        context["Client"] = self.get_queryset()
        return context

class ClientCreate(CreateView):
    """Create client"""
    model = Client
    form_class = ClientCreateForm
    template_name = "mailing/client_create.html"

    def get_context_data(self, *, object_list=None, context_object_name=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["Title"] = "Add New Client"
        return context

    def get_success_url(self, **kwargs):
        return reverse_lazy('mailing:clients')

    def form_valid(self, form):
        # save owner of user
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)

class ClientCard(DetailView):
    """Show all information about client"""
    model = Client
    template_name = "mailing/client_card.html"
    slug_url_kwarg = "client_slug"

    def get_object(self, queryset=None):
        one_client = super().get_object()
        return one_client

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["Title"] = "Client Full Information"
        context["Client"] = self.get_object()
        return context

class ClientUpdate(UpdateView):
    """Update client"""
    model = Client
    fields = ["full_name", "description", "email"]
    template_name = "mailing/client_update.html"
    slug_url_kwarg = "client_slug"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["Title"] = "Update Client"
        return context

    def get_success_url(self, **kwargs):
        return reverse_lazy('mailing:clients')

    def form_valid(self, form):
        return super().form_valid(form)

class ClientDelete(DeleteView):
    """Delete client"""
    model = Client
    template_name = "mailing/client_delete.html"
    slug_url_kwarg = "client_slug"

    def get_context_data(self, *, object_list=None, context_object_name=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["Title"] = "Delete Client"
        return context

    def get_success_url(self, **kwargs):
        return reverse_lazy('mailing:clients')




class MessagesView(ListView):
    """Show all message for owner / moderator / admin"""
    model = Messages
    template_name = "mailing/messages.html"

    def get_queryset(self):
        queryset = super().get_queryset().all()
        if not self.request.user.is_staff:
            queryset = super().get_queryset().filter(owner=self.request.user)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["Title"] = "Messages"
        context["Messages"] = self.get_queryset
        return context

class MessageCreate(CreateView):
    """Create message"""
    model = Messages
    template_name = "mailing/message_create.html"
    form_class = MessageCreateForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["Title"] = "Create Message Template"
        return context

    def get_success_url(self, **kwargs):
        return reverse_lazy('mailing:messages')

    def form_valid(self, form):
        # save owner of message
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)

class MessageUpdate(UpdateView):
    model = Messages
    fields = ["topic", "body"]
    template_name = "mailing/message_update.html"
    slug_url_kwarg = "message_slug"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["Title"] = "Update Message"
        return context

    def get_success_url(self, **kwargs):
        return reverse_lazy('mailing:messages')

    def form_valid(self, form):
        return super().form_valid(form)

class MessageDelete(DeleteView):
    model = Messages
    template_name = "mailing/message_delete.html"
    slug_url_kwarg = "message_slug"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["Title"] = "Delete Message"
        return context

    def get_success_url(self, **kwargs):
        return reverse_lazy('mailing:messages')

class MessageCard(DetailView):
    """Show all information about message"""
    model = Messages
    template_name = "mailing/message_card.html"
    slug_url_kwarg = "message_slug"

    def get_object(self, queryset=None):
        one_message = super().get_object()
        return one_message

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["Title"] = "Message Full Information"
        context["Message"] = self.get_object()
        return context


class TransferCard(DetailView):
    """Show all information about transmission"""
    model = Transfer
    template_name = "mailing/transfer_card.html"
    slug_url_kwarg = "transfer_slug"

    def get_object(self, queryset=None):
        one_transfer = super().get_object()
        return one_transfer

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["Title"] = "Transfer Full Information"
        current_object = self.get_object()
        context["Transfer"] = current_object
        # context["Statistic"] = current_object.get_statistic()
        return context
class TransferView(ListView):
    """Show all transmissions for owner / moderator / admin"""
    model = Transfer
    template_name = "mailing/transfers.html"

    def get_queryset(self):
        queryset = super().get_queryset().all()
        # if not self.request.user.is_staff:
        #     queryset = super().get_queryset().filter(owner=self.request.user)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["Title"] = "Transfers"
        context["Transfer"] = self.get_queryset()
        return context



class TransferCreate(CreateView):
    """Create transmission"""
    model = Transfer
    form_class = TransferCreateForm
    template_name = "mailing/transfer_create.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["Title"] = "Create New Transfer"
        return context

    def get_success_url(self, **kwargs):
        return reverse_lazy('mailing:transfers')

    def form_valid(self, form):

        # Create default statistic for transmission
        current_transfer = self.object
        self.object = form.save()

        # save owner of transmission
        self.object.owner = self.request.user
        self.object.save()

        # Set default data for created transmission
        Logs.objects.create(transfer_id=self.object.pk)

        # Executing send message
        schedule_transfer_time = self.object.time
        current_time = datetime.now().time()
        if schedule_transfer_time <= current_time:

            sendmails(self.object.pk,
                      self.object.client.all(),
                      self.object.message.topic,
                      self.object.message.body
                      )

            self.object.status = "FINISHED"
            self.object.save()

        return super().form_valid(form)



class TransferDelete(DeleteView):
    """Delete transmission"""
    model = Transfer
    template_name = "mailing/transfer_delete.html"
    slug_url_kwarg = "transfer_slug"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["Title"] = "Delete Transfer"
        return context

    def get_success_url(self, **kwargs):
        return reverse_lazy('mailing:transfers')


class TransferUpdate(UpdateView):
    """Update transmission"""
    model = Transfer
    fields = ["title", "time", "periodicity", "message", "client", "is_published"]
    template_name = "mailing/transfer_update.html"
    slug_url_kwarg = "transfer_slug"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["Title"] = "Update transfer"
        return context

    def get_success_url(self, **kwargs):
        return reverse_lazy('mailing:transfers')

    def form_valid(self, form):
        # check send time
        schedule_transmission_time_update = form.cleaned_data["time"]
        current_time = datetime.now().time()
        self.object.status = "CREATED"
        self.object.save()
        if schedule_transmission_time_update <= current_time and self.object.is_published is True:

            sendmails(self.object.pk,
                      self.object.client.all(),
                      self.object.message.topic,
                      self.object.message.body
                      )
            self.object.status = "FINISHED"
            self.object.save()

        return super().form_valid(form)