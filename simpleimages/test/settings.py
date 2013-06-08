import os


BASE_PATH = os.path.abspath(os.path.dirname(__file__))
MEDIA_ROOT = os.path.normpath(os.path.join(BASE_PATH, 'media'))

SECRET_KEY = 'not secret'
INSTALLED_APPS = ('simpleimages', 'simpleimages.test')
TEMPLATE_DEBUG = DEBUG = True
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'imagekit.db',
    },
}

if os.environ.get('USE_CACHE', False):
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'LOCATION': 'simpleimages'
        }
    }

# Testing

INSTALLED_APPS += ('django_nose',)
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
NOSE_ARGS = [
    '--with-specplugin',

    '--with-coverage',
    '--cover-package=simpleimages',
]
