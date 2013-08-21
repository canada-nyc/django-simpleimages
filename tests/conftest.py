import StringIO

import PIL
import pytest

from django.core.files.uploadedfile import InMemoryUploadedFile


class Image:
    def __init__(self):
        self.dimensions = (100, 100)
        self.color = 'blue'
        self.name = 'image.jpg'

    @property
    def django_file(self):
        # Create a new Django file-like object to be used in models as ImageField using
        # InMemoryUploadedFile.  If you look at the source in Django, a
        # SimpleUploadedFile is essentially instantiated similarly to what is shown here
        return InMemoryUploadedFile(self.image_file, None, self.name, 'image/jpeg',
                                    self.image_file.len, None)

    @property
    def image_file(self):
        # Create a file-like object to write thumb data (thumb data previously created
        # using PIL, and stored in variable 'thumb')
        image_io = StringIO.StringIO()
        self.pil_image.save(image_io, format='JPEG')
        image_io.seek(0)
        return image_io

    @property
    def pil_image(self):
        return PIL.Image.new('RGB', self.dimensions, self.color)


@pytest.fixture()
def image():
    return Image()
