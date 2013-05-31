from PIL import Image

from django.test import TestCase
from django.core.files.images import get_image_dimensions
from django.core.files import File
from django.core.files.base import ContentFile

from simpleimages.transforms import (scale, pil_image_from_django_file,
                                     django_file_from_pil_image)
from . import utils


class ConversionTest(TestCase):

    def test_pil_from_djange(self):
        django_image = utils.django_image(width=100, height=100)
        pil_image = pil_image_from_django_file(django_image)
        self.assertIsInstance(pil_image, Image.Image)
        self.assertItemsEqual(pil_image.size, [100, 100])

    def test_django_from_pil(self):
        pil_image = utils.pil_image(width=100, height=100)
        django_file = django_file_from_pil_image(pil_image, 'image.jpg')
        self.assertIsInstance(django_file, File)

    def test_huge_image_django_from_pil(self):
        huge_pil_image = utils.pil_image(width=5000, height=5000)
        django_file = django_file_from_pil_image(huge_pil_image, 'image.jpg')
        self.assertIsInstance(django_file, File)


class ScaleTest(utils.RemoveStorage, TestCase):
    def test_width(self):
        '''
        Make sure that if width shrinks, then height shrinks
        proportionally
        '''
        old_image = utils.django_image(width=100, height=100)
        transform = scale(width=10)
        new_image = transform(old_image)
        new_height, new_width = get_image_dimensions(new_image)
        self.assertEqual(new_height, 10)
        self.assertEqual(new_width, 10)

    def test_over_large(self):
        '''
        if specified dimension is larger than image, it shouldn't enlarge
        the image
        '''
        old_image = utils.django_image(width=100, height=100)
        transform = scale(width=200)
        new_image = transform(old_image)
        new_height, new_width = get_image_dimensions(new_image)
        self.assertEqual(new_height, 100)
        self.assertEqual(new_width, 100)

    def test_error_returns_none(self):
        old_image = ContentFile('not an image file')
        transform = scale(width=200)
        new_image = transform(old_image)
        self.assertFalse(new_image)
