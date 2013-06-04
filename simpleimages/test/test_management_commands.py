from django.test import TestCase
from django.core.management import call_command

from . import utils
from .models import TestModel
from ..trackers import track_model


class ReTransformImagesTest(utils.RemoveStorage, TestCase):
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

        self.model.thumbnail.save(
            self.image_name,
            utils.django_image(
                *self.default_dimensions,
                name=self.image_name
            ),
            save=False
        )

    def tearDown(self):
        self.disconnect()

    def test_thumb_wrong(self):
        self.assertEqual(
            self.model.thumbnail.height,
            self.default_dimensions[0],
        )

    def test_retransform_specific_model(self):
        call_command('retransform', 'test.TestModel')
        self.model_non_cached = TestModel.objects.get(pk=self.model.pk)
        self.assertEqual(
            self.model_non_cached.thumbnail.width,
            10,
        )

    def test_retransform_specific_field(self):
        call_command('retransform', 'test.TestModel.image')
        self.model_non_cached = TestModel.objects.get(pk=self.model.pk)
        self.assertEqual(
            self.model_non_cached.thumbnail.width,
            10,
        )

    def test_retransform_save_width_field(self):
        call_command('retransform', 'test.TestModel.image')
        self.model_non_cached = TestModel.objects.get(pk=self.model.pk)
        self.assertEqual(
            self.model_non_cached.thumbnail_width,
            10,
        )
