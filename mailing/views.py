from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView

import config.settings
from mailing.forms import MessageCreateForm
from mailing.models import Messages, Transfer


class MainView(LoginRequiredMixin, ListView):
    """Main page with blog and statistic"""
    model = Messages
    template_name = "mailing/massages.html"

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
    template_name = "mailing/massage_form.html"
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