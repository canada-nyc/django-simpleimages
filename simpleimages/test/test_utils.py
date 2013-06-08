from django.test import TestCase
from django.core.files.base import ContentFile

from ..utils import perform_transformation
from . import utils
from .models import TestModel


class PerformTransformationTest(utils.RemoveStorage, TestCase):
    def setUp(self):
        self.default_dimensions = (200, 200)
        self.image_name = 'image.jpg'
        self.non_image_file = ContentFile(u'some content')

        self.model = TestModel.objects.create()
        self.model2 = TestModel.objects.create()
        self.model.image.save(
            self.image_name,
            utils.django_image(
                *self.default_dimensions,
                name=self.image_name
            )
        )
        self.model2.image.save(
            '2' + self.image_name,
            utils.django_image(
                *self.default_dimensions,
                name='2' + self.image_name
            )
        )

    def test_initial_blank(self):
        self.assertFalse(self.model.thumbnail)
        self.assertFalse(self.model2.thumbnail)

    def test_transform_creates_another_image(self):
        perform_transformation([self.model])

        self.non_cached_model = TestModel.objects.get(pk=self.model.pk)
        self.non_cached_model2 = TestModel.objects.get(pk=self.model2.pk)

        self.assertTrue(self.model.thumbnail)
        self.assertFalse(self.model2.thumbnail)
        self.assertTrue(self.non_cached_model.thumbnail)
        self.assertFalse(self.non_cached_model2.thumbnail)

    def test_transformed_image_is_different(self):
        perform_transformation([self.model])

        self.non_cached_model = TestModel.objects.get(pk=self.model.pk)

        self.assertEqual(self.model.thumbnail.width, 10)
        self.assertEqual(self.non_cached_model.thumbnail.width, 10)

    def test_transform_two_instances(self):
        perform_transformation([self.model, self.model2])

        self.non_cached_model = TestModel.objects.get(pk=self.model.pk)
        self.non_cached_model2 = TestModel.objects.get(pk=self.model2.pk)

        self.assertTrue(self.model.thumbnail)
        self.assertTrue(self.model2.thumbnail)
        self.assertTrue(self.non_cached_model.thumbnail)
        self.assertTrue(self.non_cached_model2.thumbnail)

    def test_transform_queryset(self):
        perform_transformation(TestModel.objects.all())

        self.non_cached_model = TestModel.objects.get(pk=self.model.pk)
        self.non_cached_model2 = TestModel.objects.get(pk=self.model2.pk)

        self.assertTrue(self.non_cached_model.thumbnail)
        self.assertTrue(self.non_cached_model2.thumbnail)

    def test_transform_wrong_field(self):
        perform_transformation([self.model], field_names=['sdf'])

        self.non_cached_model = TestModel.objects.get(pk=self.model.pk)

        self.assertFalse(self.model.thumbnail)
        self.assertFalse(self.non_cached_model.thumbnail)

    def test_transform_right_field(self):
        perform_transformation([self.model], field_names=['image'])

        self.non_cached_model = TestModel.objects.get(pk=self.model.pk)

        self.assertTrue(self.model.thumbnail)
        self.assertTrue(self.non_cached_model.thumbnail)

    def test_transform_error_doesnt_save_file(self):
        self.model.image.save(
            self.image_name,
            self.non_image_file
        )
        perform_transformation([self.model], field_names=['image'])
        self.non_cached_model = TestModel.objects.get(pk=self.model.pk)

        self.assertTrue(self.model.image)
        self.assertTrue(self.non_cached_model.image)

        self.assertFalse(self.model.thumbnail)
        self.assertFalse(self.non_cached_model.thumbnail)

    def test_save_path(self):
        perform_transformation([self.model])
        self.assertNotIn('originals', self.model.thumbnail.path)
