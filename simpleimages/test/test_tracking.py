from django.test import TestCase

from . import utils
from .models import TestModel
from ..trackers import track_model


class ImageTransformFieldTest(utils.RemoveStorage, TestCase):
    def setUp(self):
        self.default_dimensions = (200, 200)
        self.image_name = 'image.jpg'
        self.disconnect = track_model(TestModel)
        self.model = TestModel.objects.create()
        self.model.image.save(
            self.image_name,
            utils.django_image(
                *self.default_dimensions,
                name=self.image_name
            )
        )

    def tearDown(self):
        self.disconnect()

    def test_original_image(self):
        self.assertEqual(
            self.model.image.height,
            self.default_dimensions[0],
        )
        self.assertEqual(
            self.model.image.width,
            self.default_dimensions[1],
        )

    def test_new_image_saved(self):
        self.assertTrue(
            self.model.thumbnail,
        )

    def test_new_image_transformed(self):
        self.assertEqual(
            self.model.thumbnail.width,
            10,
        )

    def test_replace_image(self):
        self.model.thumbnail.save(
            self.image_name,
            utils.django_image(
                *self.default_dimensions,
                name=self.image_name
            ),
            save=False
        )
        self.assertEqual(
            self.model.thumbnail.width,
            200,
        )
        self.model.save()
        self.assertEqual(
            self.model.thumbnail.width,
            10,
        )

    def test_image_saved_before_creation(self):
        unsaved_model = TestModel()
        unsaved_model.image.save(
            self.image_name,
            utils.django_image(
                *self.default_dimensions,
                name=self.image_name
            )
        )
        self.assertTrue(
            unsaved_model.thumbnail,
        )
