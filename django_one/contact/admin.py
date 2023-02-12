from django.contrib import admin

# Register your models here.
from .models import Contact


@admin.register(Contact)
class ContactModelAdmin(admin.ModelAdmin):
    list_display = ["topic", "email", "timestamp"]
    list_display_links = ("topic", "email")
    readonly_fields = ("topic", "email", "message")


