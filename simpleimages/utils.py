import os

from django.conf import settings


def perform_multiple_transformations(instances, field_names_to_transform=None):
    '''
    Transforms a list of models using
    :py:func:`~.utils.perform_transformation`.

    :param instances: model instances to perform transformations on.
    :type instances: iterable of instances of :py:class:`django.db.models.Model`

    :param field_names_to_transform: field names on model to perform transformations on
    :type field_names_to_transform: iterable of strings
    '''
    for instance in instances:
        perform_transformation(instance, field_names_to_transform)


def perform_transformation(instance, field_names_to_transform=None):
    '''
    Transforms a model based on the fields specified in the
    ``transformed_fields`` attribute. This should map source image
    field names to dictionaries mapping destination field name to
    their transformations. For instance::

        {
            'image': {
                'thumbnail': scale(width=10),
            }
        }

    If ``field_names_to_transform`` is None, then it will transform
    all fields. Otherwise it will only transform
    from those fields specified in ``field_names_to_transform``.

    :param instance: model instance to perform transformations on
    :type instance: instance of :py:class:`django.db.models.Model`

    :param field_names_to_transform: field names on model to perform transformations on
    :type field_names_to_transform: iterable of strings or None
    '''

    for source_field_name, destination_dict in instance.transformed_fields.items():
        if field_names_to_transform is None or source_field_name in field_names_to_transform:
            for destination_field_name, transformation in destination_dict.items():
                transform_field(instance, source_field_name, destination_field_name, transformation)


def transform_field(instance, source_field_name, destination_field_name, transformation):
    '''
    :param instance: model instance to perform transformations on
    :type instance: instance of :py:class:`django.db.models.Model`

    :param source_field_name: field name on model to find source image
    :type source_field_name: string

    :param destination_field_name: field name on model save transformed image to
    :type destination_field_name: string

    :param transformation: function, such as :py:func:`~.transforms.scale`, that takes an image files and returns a transformed image
    :type transformation: function
    '''

    source_field = getattr(instance, source_field_name)
    destination_field = getattr(instance, destination_field_name)

    OVERWRITE_EXISTING = getattr(settings, 'SIMPLEIMAGES_OVERWRITE', True)
    if not OVERWRITE_EXISTING and destination_field:
        return

    new_image = transformation(source_field)
    if new_image:
        # So that only the image file name is saved.
        # When using django-storages s3boto the name of the
        # image returns the whole path. So by using dirname
        # it will only use the actual file name when saving the
        # transformed file
        destination_name = os.path.dirname(source_field.name)
        destination_field.save(
            destination_name,
            new_image,
            save=False
        )
        instance.save(update_fields=[destination_field_name])
