from django.shortcuts import render
from django.template import RequestContext
from django.shortcuts import render_to_response
import re
from django.core.mail import send_mail
from core.forms import ContactForm

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

