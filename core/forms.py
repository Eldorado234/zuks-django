from django import forms
from core.models import ContactMail, Newsletter

class ContactForm(forms.ModelForm):
	class Meta:
		model = ContactMail
		fields = ['name', 'sender', 'sendersubject', 'content']

class NewsletterForm(forms.ModelForm):
	class Meta:
		model = Newsletter
		fields = ['subject', 'content']
