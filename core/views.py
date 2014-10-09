# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.core.mail import send_mail
from core.forms import ContactForm
from core import mail
from core.models import NewsletterRecipient
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.conf import settings
import logging

def index(request):
	form = ContactForm()
	context = RequestContext(request)
	context_dic = {"form": form}

	return render_to_response('core/index.html', context_dic, context)

def impressum(request):
	return redirect("impressum", request)

def presse(request):
	return redirect("presse",request)

def konzept(request):
	return redirect("konzept",request)

def redirect(sitename, request):
	context = RequestContext(request)
	context_dic = {}
	return render_to_response('core/' + sitename + '.html', context_dic, context)


def send_contactmail(request):
	context = RequestContext(request)

	if request.method == 'POST':
		form = ContactForm(request.POST)
		if form.is_valid():
			new_mail = form.save()
			# send Mail
			print new_mail

			text = "Absender: " + new_mail.sender + "\n" + "Datum: " + str(new_mail.contact_date) + "\n" + "Betreff: " + new_mail.sendersubject + "\n\n" + new_mail.content
			send_mail(new_mail.subject, text, new_mail.sender, [new_mail.recipient])

			return index(request)
		else:
			print form.errors
	else:
		form = ContactForm()

	return render_to_response('core/index.html', {'form': form, 'contacts': Contact.objects.all() }, context)

def subscribeToNewsletter(request):
	'''
	Called via ajax.
	'''
	context = RequestContext(request)
	context_dic = {}

	if request.method == 'POST':
		try:
			email = request.POST['email'] if 'email' in request.POST else ''

			validator = EmailValidator(message='Bitte gib eine gültige E-Mail-Adresse an.')
			validator(email)

			recp = NewsletterRecipient(email=email)
			recp.save()

			text = render_to_string('core/mail/subscribe.md', {'subscribe_id' : recp.confirm_id, 'settings' : settings})
			mail.sendMail('info@zuks.org', [recp], text, 'ZUKS Newsletter Registrierung',  display_unsubscribe=False)

			context_dic['success'] = True
		except ValidationError as e:
			context_dic['error'] = e.message
		except IntegrityError:
			context_dic['error'] = "Für diese E-Mail-Adresse wurde bereits ein Newsletter angefordert."
		except:
			logging.exception("Newsletter subscribtion failed")
			context_dic['error'] = "Die Anfrage konnte leider nicht bearbeitet werden. Versuche es später erneut."

			try:
				# Cleanup mail adress from database
				recp.delete()
			except:
				pass


	return render_to_response('core/subscribe_form.html', context_dic, context)

def confirmNewsletter(request, id):
	context = RequestContext(request)
	status = 'success'

	try:
		recp = NewsletterRecipient.objects.get(confirm_id=id)
		recp.confirm()
		recp.save()
	except NewsletterRecipient.DoesNotExist:
		status = 'expired'

	return render_to_response('core/confirm.html', {'status' : status}, context)



def unsubscribeFromNewsletter(request):
	pass
