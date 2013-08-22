import six
import PIL
import pytest

from django.core.files.base import ContentFile

import simpleimages
from .models import TestModel


class Image:
    def __init__(self):
        self.dimensions = (10, 10)
        self.color = 'blue'
        self.name = 'image.jpg'

    @property
    def django_file(self):
        return ContentFile(self.image_file.getvalue())

    @property
    def image_file(self):
        # Create a file-like object to write thumb data (thumb data previously created
        # using PIL, and stored in variable 'thumb')
        image_io = six.BytesIO()
        self.pil_image.save(image_io, format='JPEG')
        image_io.seek(0)
        return image_io

    @property
    def pil_image(self):
        return PIL.Image.new('RGB', self.dimensions, self.color)


@pytest.fixture()
def image():
    return Image()


@pytest.fixture()
def instance(db, image):
    instance = TestModel()
    instance.image.save(image.name, image.django_file)
    return instance


@pytest.fixture()
def instance_different_thumb(image, instance):
    small_dimension = instance.transform_dimension - 1
    image.dimensions = [small_dimension] * 2
    instance.thumbnail.save(image.name, image.django_file)
    assert instance.thumbnail.width != instance.image.width
    return instance


@pytest.fixture()
def transform():
    return simpleimages.transforms.BasePILTransform()


@pytest.fixture()
def transform_return_same(transform):
    transform.transform_pil_image = lambda pil_image: pil_image
    return transform
