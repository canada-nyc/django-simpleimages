import os
import sys


BASE_PATH = os.path.abspath(os.path.dirname(__file__))
MEDIA_ROOT = os.path.normpath(os.path.join(BASE_PATH, 'media'))

SECRET_KEY = 'not secret'
INSTALLED_APPS = ('simpleimages', 'tests',)
TEMPLATE_DEBUG = DEBUG = True
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
    },
}

if not sys.version_info >= (3, 0):
    INSTALLED_APPS += ('django_rq',)

    RQ_QUEUES = {
        'default': {
            'URL': 'redis://localhost:6379',
            'DB': 0,
            'ASYNC': False,
        },
    }
