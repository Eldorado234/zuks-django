from django.conf.urls import patterns, include, url
from core import views

urlpatterns = patterns('',
	url(r'^impressum/$', views.impressum, name='impressum'),
	url(r'^presse/$', views.presse, name='presse'),
	url(r'^konzept/$', views.konzept, name='konzept'),
	url(r'^$', views.index, name='index'),
	url(r'^send_contactmail/$', views.send_contactmail, name='send_contactmail'),
	url(r'^subscribe/$', views.subscribeToNewsletter, name='subscribe'),
	url(r'^confirm/(?P<id>.+)/$', views.confirmNewsletter, name='confirm'),
	url(r'^unsubscribe/(?P<id>.+)/$', views.unsubscribeFromNewsletter, name='unsubscribe'),
	url(r'^robots\.txt/$', views.robots, name='robots'),
	url(r'^sitemap\.xml/$', views.sitemap, name='sitemap'),
	url(r'^google2ba41cbba49d5958\.html/$', views.google_verification, name='google_verification'),
)
