from django.shortcuts import render
from django.template import RequestContext
from django.shortcuts import render_to_response

def index(request):
	return redirect("index", request)

def impressum(request):
	return redirect("impressum", request)

def presse(request):
	return redirect("presse",request)

def konzept(request):
	return redirect("konzept",request)

def redirect(sitename, request):
	context = RequestContext(request)
	context_dic = {}
	return render_to_response('core/'+sitename+'.html', context_dic, context)
