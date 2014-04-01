import pytest

from simpleimages.trackers import track_model
from .models import TestModel


pytestmark = pytest.mark.django_db(transaction=True)


def test_saved_creates_thumbnail(image, instance):
    disconnect = track_model(TestModel)
    instance.image.save(image.name, image.django_file)
    disconnect()
    assert instance.thumbnail


def test_saved_transforms_properly(image, instance):
    disconnect = track_model(TestModel)
    instance.image.save(image.name, image.django_file)

    disconnect()
    assert instance.thumbnail.width < image.dimensions[0]


def test_replace_image(image, instance_different_thumb):
    disconnect = track_model(TestModel)

    instance_different_thumb.image.save(image.name, image.django_file)
    disconnect()

    assert instance_different_thumb.thumbnail.width == instance_different_thumb.image.width


def test_set_dimension_field(image, instance):
    '''
    Make sure that it will set the `width_field` and `height_field` of the
    target field after transformation
    '''
    disconnect = track_model(TestModel)
    instance.image.save(image.name, image.django_file)

    disconnect()
    assert instance.thumbnail.width == instance.thumbnail_width


def test_changes_dimension_field(image, instance):
    '''
    makes sure it will override old `width_field` and `height_field` of the
    target field, when uploading a new image
    '''
    disconnect = track_model(TestModel)

    image.dimensions = (2, 2)
    instance.image.save(image.name, image.django_file)

    disconnect()
    assert instance.thumbnail_width == instance.thumbnail.width == 2


def test_saves_changed_dimension_field(image, instance):
    '''
    make sure that changes to the `width_field` and `height_field` will
    actually be saved to the databased and not only changed on the unsaved
    python instance
    '''
    disconnect = track_model(TestModel)

    image.dimensions = (2, 2)
    instance.image.save(image.name, image.django_file)

    disconnect()
    instance = instance.__class__.objects.get(pk=instance.pk)
    assert instance.thumbnail_width == instance.thumbnail.width == 2


def test_unequal_dimension_fields_saved(image, instance):
    '''
    makes sure that photos with not equal height and width dimensions will
    be correctly saved into the proper dimension fields
    '''
    disconnect = track_model(TestModel)

    image.dimensions = (1, 2)
    instance.image.save(image.name, image.django_file)

    disconnect()
    instance = instance.retrieve_from_database()
    assert instance.thumbnail_width == instance.thumbnail.width == 1
    assert instance.thumbnail_height == instance.thumbnail.height == 2
