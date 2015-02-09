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
from django.utils.translation import ugettext as _
import logging
import glob
from markdown import Markdown
from django.http import HttpResponse
import git

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
	# update subrepo
	# 1abd97cca7939d9ef1b1b904f16959cc4b010073
	faq_repo = git.cmd.Git('content/faq')
	faq_repo.pull()
	source_files = glob.glob('content/faq/*.md')
	md = Markdown()
	count = 0
	for source_path in source_files:
		target_path = 'templates/core/faq/%04d.html' % (count,)
		with open(source_path, 'r') as source, open(target_path, 'w') as target:
			html = md.convert(source.read())
			target.write(html)
		count += 1
	return HttpResponse('')

def faq(request):
	context = RequestContext(request)
	# Get all FAQ template files
	content_files = glob.glob('templates/core/faq/*.html')
	# Remove 'templates' prefix
	content_files = map(lambda x: x.split('/', 1)[1], content_files)
	return render_to_response('core/faq.html', {'content' : content_files}, context)
