# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.core.mail import send_mail
from core.forms import ContactForm, FAQForm
from core import mail
from core.models import NewsletterRecipient, FAQ
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.utils.translation import ugettext as _
import logging
from django.http import HttpResponse
from core.faq_management import FAQManagement
from threading import Thread

def index(request):
	form = ContactForm()
	context = RequestContext(request)
	context_dic = {"form": form}

	return render_to_response('core/index.html', context_dic, context)

def static(request, site, content_type="text/html"):
	return render_to_response(
		'core/{0}'.format(site),
		{},
		RequestContext(request),
		content_type=content_type
	)

def send_contactmail(request):
	'''
	Called via ajax.
	'''
	context = RequestContext(request)
	status = False

	if request.method == 'POST':
		form = ContactForm(request.POST)
		if form.is_valid():
			form.save()
			status = True
	else:
		form = ContactForm()

	return render_to_response('core/contact_form.html', {
			'form': form,
			'success': status
		}, context)

def subscribeToNewsletter(request):
	'''
	Called via ajax.
	'''
	context = RequestContext(request)
	context_dic = {}

	if request.method == 'POST':
		try:
			email = request.POST['email'] if 'email' in request.POST else ''

			validator = EmailValidator(message=_('Please enter a valid email address'))
			validator(email)

			recp = NewsletterRecipient(email=email)
			recp.save()

			text = render_to_string('core/mail/subscribe.md', {'subscribe_id' : recp.confirm_id}, context)
			mail.sendMail('info@zuks.org', [recp], text, _('ZUKS Newsletter Registration'),  display_unsubscribe=False)

			context_dic['success'] = True
		except ValidationError as e:
			context_dic['error'] = e.message
		except IntegrityError:
			context_dic['error'] = _("For this mail a newsletter is already requested.")
		except:
			logging.exception("Newsletter subscribtion failed")
			context_dic['error'] = _("Unfortunately, the request could not be processed. Please try again later.")

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

def unsubscribeFromNewsletter(request, id):
	context = RequestContext(request)

	try:
		recp = NewsletterRecipient.objects.get(confirm_id=id)
		recp.delete()
	except NewsletterRecipient.DoesNotExist:
		# Is already unsubscribed, nothing to do
		pass

	return render_to_response('core/unsubscribe.html', {}, context)

def update_faq(request):
	FAQManagement.update_faq()
    # TODO: Generate an adequate response
	return HttpResponse('')

def faq(request):
	context = RequestContext(request)
	questions = FAQ.objects.filter(consistent=True)
	params = {'questions' : questions, 'question_path': 'core/faq/', 'form': FAQForm()}
	return render_to_response('core/faq.html', params, context)

def submit_faq_question(request):
	'''
	Called via ajax.
	'''
	context = RequestContext(request)
	status = False

	if request.method == 'POST':
		form = FAQForm(request.POST)
		if form.is_valid():
			faq_question = form.save()
			status = True

			# Push question
			Thread(target=FAQManagement.push_question, args=(faq_question,)).start()
	else:
		form = FAQForm()

	return render_to_response('core/faq_form.html', {
			'form': form,
			'success': status
		}, context)
