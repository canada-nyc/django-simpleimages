import os


BASE_PATH = os.path.abspath(os.path.dirname(__file__))
MEDIA_ROOT = os.path.normpath(os.path.join(BASE_PATH, 'media'))

SECRET_KEY = 'not secret'
INSTALLED_APPS = ('simpleimages', 'tests', 'django_rq')
TEMPLATE_DEBUG = DEBUG = True
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',

        # In memory SQLite database doesn't work for RQ testing
        'NAME': os.path.join(BASE_PATH, 'sqlite-test.db'),
        'TEST_NAME': os.path.join(BASE_PATH, 'sqlite-test.db'),
    },
}

RQ_QUEUES = {
    'default': {
        'HOST': 'localhost',
        'PORT': 6379,
        'DB': 0,
    },
}
