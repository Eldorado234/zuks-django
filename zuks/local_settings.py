# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# Used to create absolute URLs (needed for e-mails)
BASE_URL = 'http://www.zuks.org'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

# You have to configure this, when DEBUG is turned off
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
# In production these files should be directly served by the webserver
STATIC_ROOT = os.path.join(PROJECT_PATH, 'static')

# Security

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '9e0b_87n@19e$rzbrnyn5jv-(q@a1ot^#^j4luaj(s)t5n0gj*'
