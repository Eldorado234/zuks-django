from django import forms
from core.models import ContactMail

class ContactForm(forms.ModelForm):
	class Meta:
		model = ContactMail
		fields = ['name', 'sender', 'sendersubject', 'content']