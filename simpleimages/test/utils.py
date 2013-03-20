import StringIO
from subprocess import call

from PIL import Image

from django.core.files.uploadedfile import InMemoryUploadedFile


def image(width=10, height=10):
    thumb = pil_image(width, height)
    # Create a file-like object to write thumb data (thumb data previously created
    # using PIL, and stored in variable 'thumb')
    thumb_io = StringIO.StringIO()
    thumb.save(thumb_io, format='JPEG')
    thumb_io.seek(0)
    return thumb_io


def pil_image(width=10, height=10):
    return Image.new('RGB', (width, height,), 'blue')


def django_image(height=10, width=10, name='name'):
    image_file = image(width, height)
    # Create a new Django file-like object to be used in models as ImageField using
    # InMemoryUploadedFile.  If you look at the source in Django, a
    # SimpleUploadedFile is essentially instantiated similarly to what is shown here
    return InMemoryUploadedFile(image_file, None, name + '.jpg', 'image/jpeg',
                                image_file.len, None)


class RemoveStorage(object):
    def tearDown(self):
        call('rm -rf testing', shell=True)
