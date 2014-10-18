#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
from datetime import datetime
from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _
from core import mail
import uuid


class NewsletterRecipient(models.Model):
	class Meta:
		verbose_name = _("Newsletter Recipient")
		verbose_name_plural = _("Newsletter Recipients")

	email = models.EmailField(unique=True, verbose_name=_("Email address"))
	confirm_id = models.CharField(max_length=36, default=uuid.uuid4(), unique=True, verbose_name=_("Confirmation identifier"), help_text=_("Id the recipient could use to confirm his Email address and unregister the newsletter"))
	register_date = models.DateTimeField(auto_now_add=True, verbose_name=_("Registration date"))
	confirmed = models.BooleanField(default=False, verbose_name=_("Confirmation status"))
	confirm_date = models.DateTimeField(null=True, blank=True, verbose_name=_("Confirmation date"))

	def confirm(self):
		self.confirmed = True
		self.confirm_date = datetime.now()

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
		mail.sendMail(self.sender, recipients, self.content, self.subject)

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
