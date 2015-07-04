# This file is part of ZUKS-Website.
#
# ZUKS-Website is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# ZUKS-Website is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with ZUKS-Website. If not, see <http://www.gnu.org/licenses/>.

from django.contrib import admin
from django.template import RequestContext
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.conf.urls import patterns, url
from core import mail
from core.models import Newsletter, NewsletterRecipient, ContactMail
from core.forms import NewsletterForm
from django.contrib import messages
from django.utils.translation import ugettext as _

class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('subject', 'content', 'send_date')
    list_display_links = None

    def add_view(self, request):
        context = RequestContext(request)
        if request.POST:
            form = NewsletterForm(request.POST)
            if form.is_valid():
                form.save()

                # Add feedback for the user and return to the newsletter
                # overview page
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    _('Newsletter successfully sent')
                )
                return redirect('admin:core_newsletter_changelist')
        else:
            form = NewsletterForm()
        return render_to_response('core/newsletter_backend.html', {'form' : form}, context)

    def newsletter_template(self, request):
        context = RequestContext(request)

        content = request.POST['content'] if request.POST else ''
        (_,html) = mail.renderContent(content, 0, 'placeholder', context=context)

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
        return my_urls + urls

class NewsletterRecipientAdmin(admin.ModelAdmin):
    list_display = ('email', 'confirmed', 'register_date', 'confirm_date')

class ContactMailAdmin(admin.ModelAdmin):
    list_display = ('name', 'sendersubject', 'sender', 'contact_date')

admin.site.register(Newsletter, NewsletterAdmin)
admin.site.register(NewsletterRecipient, NewsletterRecipientAdmin)
admin.site.register(ContactMail, ContactMailAdmin)
