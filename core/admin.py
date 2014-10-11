from django.contrib import admin
from django.template import RequestContext
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.conf.urls import patterns, url
from core import mail
from core.models import Newsletter, NewsletterRecipient, ContactMail
from core.forms import NewsletterForm

class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('subject', 'content', 'send_date')
    list_display_links = None

    def add_view(self, request):
        context = RequestContext(request)
        if request.POST:
            form = NewsletterForm(request.POST)
            if form.is_valid():
                form.save()
        else:
            form = NewsletterForm()
        return render_to_response('core/newsletter_backend.html', {'form' : form}, context)

    def newsletter_template(self, request):
        content = request.POST['content'] if request.POST else ''
        (_,html) = mail.renderContent(content, 'placeholder')

        return HttpResponse(html)

    def get_urls(self):
        urls = super(NewsletterAdmin, self).get_urls()
        my_urls = patterns('',
            url(
                r'^newsletter-template/$',
                self.admin_site.admin_view(self.newsletter_template),
                name='newsletter-template'
            ),
        )
        print my_urls + urls
        return my_urls + urls

class ContactMailAdmin(admin.ModelAdmin):
    list_display = ('name', 'sendersubject', 'sender', 'contact_date')

admin.site.register(Newsletter, NewsletterAdmin)
admin.site.register(NewsletterRecipient)
admin.site.register(ContactMail, ContactMailAdmin)
