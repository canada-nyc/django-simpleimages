from simpleimages.trackers import track_model
from .models import TestModel


def test_saved_creates_thumbnail(db, image, instance):
    disconnect = track_model(TestModel)
    instance.image.save(image.name, image.django_file)
    disconnect()
    assert instance.thumbnail


def test_saved_transforms_properly(db, image, instance):
    disconnect = track_model(TestModel)
    instance.image.save(image.name, image.django_file)

    disconnect()
    assert instance.thumbnail.width < image.dimensions[0]


def test_replace_image(db, image, instance_different_thumb):
    disconnect = track_model(TestModel)

    instance_different_thumb.image.save(image.name, image.django_file)
    disconnect()

    assert instance_different_thumb.thumbnail.width == instance_different_thumb.image.width


def test_set_dimension_field(db, image, instance):
    '''
    Make sure that it will set the `width_field` and `height_field` of the
    target field after transformation
    '''
    disconnect = track_model(TestModel)
    instance.image.save(image.name, image.django_file)

    disconnect()
    assert instance.thumbnail.width == instance.thumbnail_width


def test_changes_dimension_field(db, image, instance):
    '''
    makes sure it will override old `width_field` and `height_field` of the
    target field, when uploading a new image
    '''
    disconnect = track_model(TestModel)

    image.dimensions = (2, 2)
    instance.image.save(image.name, image.django_file)
    old_thumbnail_width_field = instance.thumbnail_width
    assert old_thumbnail_width_field == instance.thumbnail.width == 2

    image.dimensions = (10, 10)
    instance.image.save(image.name, image.django_file)
    new_thumbnail_width_field = instance.thumbnail_width

    assert new_thumbnail_width_field == instance.thumbnail.width == 5

    disconnect()
