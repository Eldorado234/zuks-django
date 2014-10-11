from django.conf.urls import patterns, include, url
from core import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),

	url(r'^impressum/$', views.static, {'site' : 'impressum.html'}, name='impressum'),
	url(r'^presse/$', views.static, {'site' : 'impressum.html'}, name='presse'),
	url(r'^konzept/$', views.static, {'site' : 'konzept.html'}, name='konzept'),

	url(r'^send_contactmail/$', views.send_contactmail, name='send_contactmail'),

	url(r'^subscribe/$', views.subscribeToNewsletter, name='subscribe'),
	url(r'^confirm/(?P<id>.+)/$', views.confirmNewsletter, name='confirm'),
	url(r'^unsubscribe/(?P<id>.+)/$', views.unsubscribeFromNewsletter, name='unsubscribe'),

	url(r'^robots\.txt/$', views.static, {'site' : 'robots.txt', 'content_type' : 'text/plain'}, name='robots'),
	url(r'^sitemap\.xml/$', views.static, {'site' : 'sitemap.xml', 'content_type' : 'text/xml'}, name='sitemap'),
	url(r'^google2ba41cbba49d5958\.html/$', views.static, {'site' : 'google2ba41cbba49d5958.html'}, name='google_verification'),
)
