import pytest

from django.core.files.images import get_image_dimensions

from .models import TestModel


class TestTransformField:
    @pytest.fixture()
    def instance(self, db):
        return TestModel.objects.create()

    @pytest.fixture()
    def instance_with_source(self, image, instance):
        instance.image.save(image.name, image.django_file)
        return instance

    @pytest.fixture()
    def instance_with_source_and_thumb(self, image, instance_with_source):
        source_dimensions = get_image_dimensions(instance_with_source.image)
        image.dimensions = [dimension + 1 for dimension in source_dimensions]
        instance_with_source.thumbnail.save(image.name, image.django_file)
        return instance_with_source

    def test_blank_transform_wont_save(self, instance_with_source):
        instance_with_source._transform(lambda file: None)

        assert not instance_with_source.thumbnail

    def test_will_save(self, instance_with_source):
        instance_with_source._transform()

        assert instance_with_source.thumbnail

    def test_no_overwrite(self, settings, instance_with_source_and_thumb):
        settings.SIMPLEIMAGES_OVERWRITE = False

        instance_with_source_and_thumb._transform()

        assert not instance_with_source_and_thumb.thumbnail.width == instance_with_source_and_thumb.image.width

    def test_yes_overwrite(self, settings, instance_with_source_and_thumb):
        settings.SIMPLEIMAGES_OVERWRITE = True

        instance_with_source_and_thumb._transform()

        assert instance_with_source_and_thumb.thumbnail.width == instance_with_source_and_thumb.image.width
