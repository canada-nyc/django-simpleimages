import six
import PIL
import pytest
import shutil

from django.core.files.base import ContentFile
from django.conf import settings

import simpleimages
import simpleimages.trackers
from .models import TestModel


class Image:

    def __init__(self):
        self.width, self.height = (10, 10)
        self.color = 'blue'
        self.name = 'image.jpg'

    @property
    def dimensions(self):
        return self.width, self.height

    @dimensions.setter
    def dimensions(self, value):
        self.width, self.height = value

    @property
    def django_file(self):
        return ContentFile(self.image_file.getvalue())

    @property
    def image_file(self):
        # Create a file-like object to write thumb data (thumb data previously
        # created using PIL, and stored in variable 'thumb')
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


def remove_media():
    shutil.rmtree(settings.MEDIA_ROOT)


@pytest.fixture()
def instance_no_image(image, request):
    request.addfinalizer(remove_media)
    return TestModel()


@pytest.fixture()
def instance(image, request):
    request.addfinalizer(remove_media)
    instance = TestModel()

    assert not instance.thumbnail

    instance.image.save(image.name, image.django_file)
    return instance


@pytest.fixture()
def instance_undersized(image, request):
    request.addfinalizer(remove_media)
    instance = TestModel()
    image.width = instance.transform_max_width - 1

    instance.image.save(image.name, image.django_file)
    return instance


@pytest.fixture()
def instance_oversized(image, request):
    request.addfinalizer(remove_media)
    instance = TestModel()
    image.width = instance.transform_max_width + 1

    instance.image.save(image.name, image.django_file)
    return instance


@pytest.fixture()
def instance_larger_thumb(image, instance):
    image.width = instance.transform_max_width + 1
    instance.thumbnail.save(image.name, image.django_file)
    return instance


@pytest.fixture(scope="module")
def track_model(request):
    disconnect = simpleimages.trackers.track_model(TestModel)

    request.addfinalizer(disconnect)


@pytest.fixture()
def transform():
    return simpleimages.transforms.BasePILTransform()


@pytest.fixture()
def transform_return_same(transform):
    transform.transform_pil_image = lambda pil_image: pil_image
    return transform
