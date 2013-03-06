from django.utils import unittest
from django.core.files.images import get_image_dimensions

from simpleimages import transforms
from . import utils


class ScaleTest(unittest.TestCase):
    def test_width(self):
        '''
        Make sure that if width shrinks, then height shrinks
        proportionally
        '''
        old_image = utils.image(width=100, height=100)
        transform = transforms.scale(width=10)
        new_image = transform(old_image)
        new_height, new_width = get_image_dimensions(new_image)
        self.assertEqual(new_height, 10)
        self.assertEqual(new_width, 10)

    def test_over_large(self):
        '''
        if specified dimension is larger than image, it shouldn't enlarge
        the image
        '''
        old_image = utils.image(width=100, height=100)
        transform = transforms.scale(width=200)
        new_image = transform(old_image)
        new_height, new_width = get_image_dimensions(new_image)
        self.assertEqual(new_height, 100)
        self.assertEqual(new_width, 100)
