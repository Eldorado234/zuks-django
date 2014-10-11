from django.contrib import admin

from core.models import Newsletter, NewsletterRecipient, ContactMail

admin.site.register(Newsletter)
admin.site.register(NewsletterRecipient)
admin.site.register(ContactMail)
