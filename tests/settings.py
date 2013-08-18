import os


BASE_PATH = os.path.abspath(os.path.dirname(__file__))
MEDIA_ROOT = os.path.normpath(os.path.join(BASE_PATH, 'media'))

SECRET_KEY = 'not secret'
INSTALLED_APPS = ('simpleimages',)
TEMPLATE_DEBUG = DEBUG = True
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'imagekit.db',
    },
}
