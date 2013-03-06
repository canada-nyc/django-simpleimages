import StringIO

from PIL import Image

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.conf import settings
from django.core.management import call_command
from django.db.models import loading


def image(width=10, height=10):
    thumb = Image.new('RGB', (width, height,), 'blue')
    # Create a file-like object to write thumb data (thumb data previously created
    # using PIL, and stored in variable 'thumb')
    thumb_io = StringIO.StringIO()
    thumb.save(thumb_io, format='JPEG')
    thumb_io.seek(0)
    return thumb_io


def django_image(height=10, width=10, name='name'):
    image_file = image(width, height)
    # Create a new Django file-like object to be used in models as ImageField using
    # InMemoryUploadedFile.  If you look at the source in Django, a
    # SimpleUploadedFile is essentially instantiated similarly to what is shown here
    return InMemoryUploadedFile(image_file, None, name + '.jpg', 'image/jpeg',
                                image_file.len, None)


class AddTestApp(object):
    custom_apps = ('simpleimages.test')

    def _pre_setup(self):
        # Add the models to the db.
        self._original_installed_apps = list(settings.INSTALLED_APPS)
        settings.INSTALLED_APPS += self.custom_apps
        loading.cache.loaded = False
        call_command('syncdb', interactive=False, verbosity=0, migrate=False)
        # Call the original method that does the fixtures etc.
        super(AddTestApp, self)._pre_setup()

    def _post_teardown(self):
        # Call the original method.
        super(AddTestApp, self)._post_teardown()
        # Restore the settings.
        settings.INSTALLED_APPS = self._original_installed_apps
        loading.cache.loaded = False
