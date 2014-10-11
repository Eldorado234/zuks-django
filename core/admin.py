from django.contrib import admin

from core.models import Newsletter, NewsletterRecipient, ContactMail

class NewsletterAdmin(admin.ModelAdmin):
  list_display = ('subject', 'send_date')

class ContactMailAdmin(admin.ModelAdmin):
	list_display = ('name', 'sendersubject', 'sender', 'contact_date')

admin.site.register(Newsletter, NewsletterAdmin)
admin.site.register(NewsletterRecipient)
admin.site.register(ContactMail, ContactMailAdmin)
