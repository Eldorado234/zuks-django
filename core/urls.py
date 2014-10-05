from django.conf.urls import patterns, include, url
from core import views

urlpatterns = patterns('',
	url(r'^impressum/$', views.impressum, name='impressum'),
	url(r'^presse/$', views.presse, name='presse'),
	url(r'^konzept/$', views.konzept, name='konzept'),
	url(r'^$', views.index, name='index'),
	url(r'^send_contactmail/$', views.send_contactmail, name='send_contactmail'),
	url(r'^unsubscribe/(?P<id>.+)/$', views.unsubscribeFromNewsletter, name='unsubscribe'),
)
