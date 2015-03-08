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
	# Update FAQ repository
	faq_repo = git.cmd.Git('content/faq')
	faq_repo.pull()

	# Reset consistency status of all FAQ questions.
	# If no question exists for an question entry, the question will 
	# remain inconsistent and is not shown in the FAQ. 
	# It could be aded later again, the author information will remain.
	for question in FAQ.objects.all():
		question.consistent = False
	
	source_files = glob.glob('content/faq/*.md')
	md = Markdown()
	for source_path in source_files:
		file_name = os.path.basename(source_path)

		# Check for database consistency
		try:
			question = FAQ.objects.get(file_name=file_name)
			question.consistent = True
		except FAQ.DoesNotExist:
			# Question was added directly in the repository
			# Assume, that this question was authored by ZUKS
			FAQ.objects.create(	file_name=file_name,
								author=_("ZUKS"),
								email=_("@zuks-mail"),
								twitter_handle=_("@zuks-twitter"),
								consistent=True)

		# Convert markdown to html files
		target_path = 'templates/core/faq/%s.html' % (file_name,)
		with open(source_path, 'r') as source, open(target_path, 'w') as target:
			html = md.convert(source.read())
			target.write(html)

	return HttpResponse('')

def faq(request):
	context = RequestContext(request)
	# Get all FAQ template files
	content_files = glob.glob('templates/core/faq/*.html')
	# Remove 'templates' prefix
	content_files = map(lambda x: x.split('/', 1)[1], content_files)
	return render_to_response('core/faq.html', {'content' : content_files}, context)
