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

"""
DEVELOPMENT SAMPLE
------------------
Do NOT change this file. Create a copy with the name 'local_settings.py'
and enter your environment specific settings there.

This sample settings file is for a DEVELOPMENT environment. Use the
'production_settings.sample.py' for production.

"""

"""
Local Django settings for zuks project.

These settings are environment specific and should not be submitted or
published.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

import os
from zuks.settings import BASE_DIR
from zuks.settings import PROJECT_PATH

# Used to create absolute URLs (needed for e-mails)
BASE_URL = 'http://yourhost.de'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

# The path, where static files should be copied by collectstatic
STATIC_ROOT = os.path.join(PROJECT_PATH, 'static')

# Security

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'GENERATED KEY HERE'
