#!/usr/bin/env python
# -*- coding: utf-8 -*-
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

from django.db import models
from datetime import datetime
from django.conf import settings
from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _
from core import mail
import pytz
import hashlib


class NewsletterRecipient(models.Model):
	class Meta:
		verbose_name = _("Newsletter Recipient")
		verbose_name_plural = _("Newsletter Recipients")

	email = models.EmailField(unique=True, verbose_name=_("Email address"))
	confirm_id = models.CharField(max_length=40, unique=True, verbose_name=_("Confirmation identifier"), help_text=_("Id the recipient could use to confirm his Email address and unregister the newsletter"))
	register_date = models.DateTimeField(auto_now_add=True, verbose_name=_("Registration date"))
	confirmed = models.BooleanField(default=False, verbose_name=_("Confirmation status"))
	confirm_date = models.DateTimeField(null=True, blank=True, verbose_name=_("Confirmation date"))

	def confirm(self):
		self.confirmed = True
		# as we work with the local times, we have to set it with the correct timezone.
		self.confirm_date = datetime.now().replace(tzinfo=pytz.timezone(settings.TIME_ZONE)) if settings.USE_TZ else datetime.now()

	def save(self, *args, **kwargs):
		src = (self.email + datetime.now().isoformat()).encode('utf-8')
		self.confirm_id = hashlib.sha1(src).hexdigest()

		super(NewsletterRecipient, self).save(*args, **kwargs)


	def __unicode__(self):
		return self.email;

class Newsletter(models.Model):
	class Meta:
		verbose_name = _("Newsletter")
		verbose_name_plural = _("Newsletters")

	sender = "info@zuks.org"

	content = models.TextField(verbose_name=_("Content"))
	subject = models.CharField(max_length=100, verbose_name=_("Subject"))
	send_date = models.DateTimeField(auto_now_add=True, verbose_name=_("Send date"))

	def __unicode__(self):
		return self.subject

	def save(self, *args, **kwargs):
		super(Newsletter, self).save(*args, **kwargs)

		# Send mails
		recipients = NewsletterRecipient.objects.filter(confirmed=True)
		mail.sendMail(self.sender, recipients, self.content, self.subject, skip_errors=True)

class ContactMail(models.Model):
	class Meta:
		verbose_name = _("Contact Mail")
		verbose_name_plural = _("Contact Mails")

	recipient = "info@zuks.org"
	subject = _("ZUKS Contact request")
	text_pattern = _("Sender: %(sender)s\nDate: %(date)s\nSubject: %(subject)s\n\n%(content)s")

	name = models.CharField(max_length=100, verbose_name=_("Name"))
	sender = models.EmailField(max_length=128, verbose_name=_("Email address"))
	contact_date = models.DateTimeField(auto_now_add=True, verbose_name=_("Date"))
	sendersubject = models.CharField(max_length=100, verbose_name=_("Subject"))
	content = models.TextField(verbose_name=_("Text"))

	def __unicode__(self):
		return self.subject

	def save(self, *args, **kwargs):
		super(ContactMail, self).save(*args, **kwargs)

		# Send mail
		text = self.text_pattern % {
			'sender' : self.sender,
			'date' 	: str(self.contact_date),
			'subject' : self.sendersubject,
			'content' : self.content
		}
		send_mail(self.subject, text, self.sender, [self.recipient])
