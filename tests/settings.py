import os


BASE_PATH = os.path.abspath(os.path.dirname(__file__))
MEDIA_ROOT = os.path.normpath(os.path.join(BASE_PATH, 'media'))

SECRET_KEY = 'not secret'
INSTALLED_APPS = ('simpleimages', 'tests', 'django_rq', 'kombu.transport.django')

TEMPLATE_DEBUG = DEBUG = True
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgres',
        'USER': 'postgres',
        'HOST': os.environ['DB_HOST'],
        'PORT': 5432,
    }
}

RQ_QUEUES = {
    'default': {
        'HOST': os.environ['REDIS_HOST'],
        'PORT': 6379,
        'DB': 0,
    },
}


BROKER_URL = 'django://'
