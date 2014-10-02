#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
from datetime import datetime
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

	content = models.TextField(help_text="Der Inhalt des Newsletters")
	subject = models.CharField(max_length=100, help_text="Der Betreff des Newsletters")
	send_date = models.DateTimeField(auto_now_add=True, help_text="Das Datum, an dem der Newsletter versand wurde")

	def __unicode__(self):
		return self.subject