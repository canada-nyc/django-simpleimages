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
