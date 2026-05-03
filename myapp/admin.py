from django.contrib import admin
from .models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'received_at')
    readonly_fields = ('name', 'email', 'message', 'received_at')
    ordering = ('-received_at',)
