from django.contrib import admin
from mailing.models import Client, Transfer, Messages, Logs


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email',)
    search_fields = ('full_name',)


@admin.register(Transfer)
class TransferAdmin(admin.ModelAdmin):
    list_display = ('title', 'time', 'periodicity', 'status', 'is_published')
    list_filter = ('is_published',)
    search_fields = ('title',)


@admin.register(Messages)
class MessagesAdmin(admin.ModelAdmin):
    list_display = ('topic', )
    list_filter = ('topic',)
    search_fields = ('topic',)



@admin.register(Logs)
class LogsAdmin(admin.ModelAdmin):
    list_display = ('time', 'status', 'mail_answer')
