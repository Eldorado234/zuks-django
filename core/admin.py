from django.contrib import admin

from core.models import Newsletter, NewsletterRecipient

admin.site.register(Newsletter)
admin.site.register(NewsletterRecipient)