from django.contrib import admin

from .models import ContactFormSubmission


@admin.register(ContactFormSubmission)
class ContactFormSubmissionAdmin(admin.ModelAdmin):
    list_display = ["datetime", "name", "email", "phone", "ip_address"]
    list_display_links = ["name"]
    ordering = ["-datetime"]
