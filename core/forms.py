from django import forms
from core.models import ContactMail, Newsletter, FAQ
from django.utils.translation import ugettext_lazy as _

class ContactForm(forms.ModelForm):
	class Meta:
		model = ContactMail
		fields = ['name', 'sender', 'sendersubject', 'content']

class NewsletterForm(forms.ModelForm):
	class Meta:
		model = Newsletter
		fields = ['subject', 'content']

class FAQForm(forms.ModelForm):
    class Meta:
        model = FAQ
        fields = ['author', 'email', 'twitter_handle', 'text']