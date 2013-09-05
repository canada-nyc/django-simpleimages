import os

from django.conf import settings
try:
    from django.utils.module_loading import import_by_path
except:  # Added in Django 1.6
    from simpleimages.django_compat import import_by_path


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


def get_caller():
    caller_text = getattr(
        settings,
        'SIMPLEIMAGES_TRANSFORM_CALLER',
        'simpleimages.callers.default'
    )
    return import_by_path(caller_text)


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
                arguments = [instance, source_field_name, destination_field_name, transformation]
                get_caller()(transform_field, *arguments)


def transform_field(instance, source_field_name, destination_field_name, transformation):
    '''
    Does an image transformation on a instance. It will get the image
    from the source field attribute of the instnace, then call
    the transformation function with that instance, and finally
    save that transformed image into the destination field attribute
    of the instance.

    .. note::

    If either the source field is blank, or the transformation returns
    a false value then the destination field will be deleted.

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

    transformed_image = get_transformed_image(source_field, transformation)
    if transformed_image:
        destination_name = os.path.basename(source_field.name)

        destination_field.save(
            destination_name,
            transformed_image,
            save=False
        )
    else:
        destination_field.delete()
    instance.save(update_fields=[destination_field_name])


def get_transformed_image(source, transformation):
    if source:
        source.open()
        return transformation(source)
