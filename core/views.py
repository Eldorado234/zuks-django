# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.http import Http404, HttpResponse
from django.utils.translation import ugettext as _
from django.core.mail import send_mail
from django.utils.html import escape
from django.utils.safestring import mark_safe
from markdown import Markdown
from core.forms import ContactForm
from core import mail
from core.models import NewsletterRecipient, Newsletter
import logging

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
			mail.sendMail('info@zuks.org', [recp], text, None, _('ZUKS Newsletter Registration'),  display_unsubscribe=False)

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

def viewNewsletter(request, newsId, user = None):
	context = RequestContext(request)

	try:
		news = Newsletter.objects.get(id=newsId)
	except Newsletter.DoesNotExist:
		raise Http404(_('Newsletter could not be found.'))

	if user is not None:
		usr = NewsletterRecipient.objects.get(confirm_id=user)
	else:
		usr = None

	unsubscribeId = usr.confirm_id if usr is not None else None
	mailContent = mark_safe(Markdown().convert(escape(news.content)))
	(txt, mailContent) = mail.renderContent(news.content, newsId, unsubscribeId, tpl='core/mail/news_body.html')
	# remove <html>/<body>/<head> data.
	mailContent = mailContent.replace('<html>', '').replace('</html>', '').replace('<head></head>', '').replace('</body>', '')
	mailContent = mailContent[mailContent.index('>', mailContent.index('<body'))+1:]

	return render_to_response(
		'core/newsletter.html', {
			'news': news,
			'newsContent': mailContent,
			'newsId': newsId,
			'userId': user,
		}, context
	)