from django.utils import unittest
from django.core.files.images import ImageFile

from . import utils
from .models import TestModel


class ImageTransformFieldTest(utils.AddTestApp, unittest.TestCase):
    def setUp(self):
        self.model = TestModel.objects.create()
        self.default_dimensions = (10, 10)
        self.model.image.save(
            utils.django_image(
                *self.default_dimensions,
                name='image.jpg'
            )
        )

    def test_original_image(self):
        self.assertEqual(
            self.model.image.height,
            self.default_dimensions[0],
        )
        self.assertEqual(
            self.model.image.width,
            self.default_dimensions[1],
        )
        self.assertIsInstance(
            self.models.image,
            ImageFile
        )
        self.assertEqual(
            self.models.image.path,
            'store/product_images/image.jpg'
        )

    def test_new_image_saved(self):
        self.assertIn('large', self.model.image.thumbs)
        self.assertIsInstance(
            self.models.image.thumbs['large'],
            ImageFile
        )

    def test_new_image_transformed(self):
        new_image = self.models.image.thumbs['large']
        self.assertEqual(
            new_image.height,
            20,
        )

    def test_new_image_path(self):
        new_image = self.models.image.thumbs['large']
        self.assertEqual(
            new_image.path,
            'store/product_images/image_large.jpg'
        )
