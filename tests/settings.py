import os


BASE_PATH = os.path.abspath(os.path.dirname(__file__))
MEDIA_ROOT = os.path.normpath(os.path.join(BASE_PATH, 'media'))

SECRET_KEY = 'not secret'
INSTALLED_APPS = ('simpleimages', 'tests', 'django_rq', 'pq')
TEMPLATE_DEBUG = DEBUG = True
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'django_simpleimages',
        'USER': 'postgres',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

RQ_QUEUES = {
    'default': {
        'HOST': 'localhost',
        'PORT': 6379,
        'DB': 0,
    },
}
