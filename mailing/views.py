from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

import config.settings
from mailing.models import Messages, Transfer


class MainView(LoginRequiredMixin, ListView):
    """Main page with blog and statistic"""
    model = Messages
    template_name = "mailing/main.html"

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
