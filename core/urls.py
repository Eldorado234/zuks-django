# This file is part of ZUKS-Website.
#
# ZUKS-Website is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# ZUKS-Website is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with ZUKS-Website. If not, see <http://www.gnu.org/licenses/>.

from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView
from core import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),

	url(r'^impressum/$', views.static, {'site' : 'impressum.html'}, name='impressum'),
	url(r'^presse/$', RedirectView.as_view(url='https://zuks.totemapp.com/', permanent=True), name='presse'),
	url(r'^konzept/$', views.static, {'site' : 'konzept.html'}, name='konzept'),

	url(r'^send_contactmail/$', views.send_contactmail, name='send_contactmail'),

	url(r'^subscribe/$', views.subscribeToNewsletter, name='subscribe'),
	url(r'^confirm/(?P<id>.+)/$', views.confirmNewsletter, name='confirm'),
	url(r'^unsubscribe/(?P<id>.+)/$', views.unsubscribeFromNewsletter, name='unsubscribe'),

	url(r'^robots\.txt/$', views.static, {'site' : 'robots.txt', 'content_type' : 'text/plain'}, name='robots'),
	url(r'^sitemap\.xml/$', views.static, {'site' : 'sitemap.xml', 'content_type' : 'text/xml'}, name='sitemap'),
	url(r'^google2ba41cbba49d5958\.html/$', views.static, {'site' : 'google2ba41cbba49d5958.html'}, name='google_verification'),
)
