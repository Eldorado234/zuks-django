from django.shortcuts import render
from django.template import RequestContext
from django.shortcuts import render_to_response

def index(request):
	context = RequestContext(request)
	context_dic = {}
	return render_to_response('core/index.html', context_dic, context)
