#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
from datetime import datetime
from django.core.mail import send_mail
from core import mail
import uuid


class NewsletterRecipient(models.Model):

	email = models.EmailField(unique=True, help_text="Die E-Mail-Adresse des Empfängers")
	confirm_id = models.CharField(max_length=36, default=uuid.uuid4(), unique=True, help_text="Diese ID dient dazu die E-Mail-Adresse des Empfängers zu bestätigen.")
	register_date = models.DateTimeField(auto_now_add=True, help_text="Das Datum, an dem sich der Empfänger für den Newsletter registriert hat")
	confirmed = models.BooleanField(default=False, help_text="Gibt an, ob der Empfänger seine E-Mail-Adresse bereits bestätigt hat.")
	confirm_date = models.DateTimeField(null=True, blank=True, help_text="Das Datum, an dem der seine E-Mail-Adresse bestätigt hat")

	def confirm(self):
		self.confirmed = True
		self.confirm_date = datetime.now()

	def __unicode__(self):
		return self.email;

class Newsletter(models.Model):
	sender = "info@zuks.org"

	content = models.TextField(help_text="Der Inhalt des Newsletters")
	subject = models.CharField(max_length=100, help_text="Der Betreff des Newsletters")
	send_date = models.DateTimeField(auto_now_add=True, help_text="Das Datum, an dem der Newsletter versand wurde")

	def __unicode__(self):
		return self.subject

	def save(self, *args, **kwargs):
		super(Newsletter, self).save(*args, **kwargs)

		# Send mails
		recipients = NewsletterRecipient.objects.filter(confirmed=True)
		mail.sendMail(self.sender, recipients, self.content, self.subject, skip_errors=True)

class ContactMail(models.Model):
	recipient = "info@zuks.org"
	subject = "ZUKS Kontaktanfrage"
	text_pattern = "Absender: {0}\nDatum: {1}\nBetreff: {2}\n\n{3}"

	name = models.CharField(max_length=100, verbose_name="Name")
	sender = models.EmailField(max_length=128, verbose_name="Email-Adresse")
	contact_date = models.DateTimeField(auto_now_add=True, verbose_name="Datum")
	sendersubject = models.CharField(max_length=100, verbose_name="Betreff")
	content = models.TextField(verbose_name="Anliegen")

	def __unicode__(self):
		return self.subject

	def save(self, *args, **kwargs):
		super(ContactMail, self).save(*args, **kwargs)

		# Send mail
		text = self.text_pattern.format(
			self.sender,
			str(self.contact_date),
			self.sendersubject,
			self.content
		)
		send_mail(self.subject, text, self.sender, [self.recipient])
