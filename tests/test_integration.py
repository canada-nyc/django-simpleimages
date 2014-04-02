import pytest


pytestmark = [
    pytest.mark.django_db(transaction=True),
    pytest.mark.usefixtures("track_model"),
]


def test_saved_creates_thumbnail(image, instance):
    assert instance.thumbnail


def test_saved_transforms_properly(image, instance_oversized):

    assert instance_oversized.thumbnail.width < instance_oversized.image.width


def test_replace_image(image, instance_undersized):

    assert instance_undersized.thumbnail.width == instance_undersized.image.width

    image.width = instance_undersized.transform_max_width + 1

    instance_undersized.image.save(image.name, image.django_file)

    assert instance_undersized.thumbnail.width < instance_undersized.image.width


def test_set_dimension_field(image, instance):
    '''
    Make sure that it will set the `width_field` and `height_field` of the
    target field after transformation
    '''
    assert instance.thumbnail.width == instance.thumbnail_width


def test_changes_dimension_field(image, instance_undersized):
    '''
    makes sure it will override old `width_field` and `height_field` of the
    target field, when uploading a new image
    '''

    image.width = instance_undersized.thumbnail.width - 1
    instance_undersized.image.save(image.name, image.django_file)

    assert instance_undersized.thumbnail_width == instance_undersized.thumbnail.width == image.width


def test_saves_changed_dimension_field(image, instance):
    '''
    make sure that changes to the `width_field` and `height_field` will
    actually be saved to the databased and not only changed on the unsaved
    python instance
    '''

    image.width = instance.transform_max_width - 1
    instance.image.save(image.name, image.django_file)

    instance = instance.retrieve_from_database()

    assert instance.thumbnail_width == instance.thumbnail.width == image.width


def test_unequal_dimension_fields_saved(image, instance):
    '''
    makes sure that photos with not equal height and width dimensions will
    be correctly saved into the proper dimension fields
    '''
    max_width = instance.transform_max_width
    image.dimensions = (max_width - 1, max_width - 2)
    instance.image.save(image.name, image.django_file)

    instance = instance.retrieve_from_database()

    assert instance.thumbnail_width == instance.thumbnail.width == image.width
    assert instance.thumbnail_height == instance.thumbnail.height == image.height


def test_oversized_image_saves_changed_dimensions(image, instance):
    '''
    if a photo is too large, make sure the resized version updates the dimension
    fields
    '''
    max_width = instance.transform_max_width
    image.width = max_width * 2
    image.height = max_width
    instance.image.save(image.name, image.django_file)

    instance = instance.retrieve_from_database()

    assert instance.thumbnail_width == instance.thumbnail.width == image.width / 2
    assert instance.thumbnail_height == instance.thumbnail.height == image.height / 2
