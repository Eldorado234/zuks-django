from django.conf.urls import patterns, include, url

from core import views

urlpatterns = patterns('',
	url(r'^impressum/$', views.impressum, name='impressum'),
	url(r'^presse/$', views.presse, name='presse'),
	url(r'^konzept/$', views.konzept, name='konzept'),
	url(r'^$', views.index, name='index'),
)
