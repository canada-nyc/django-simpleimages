Usage
=====

Models
---------

Here is an example model that will create transformed images on save::

    from django.db import models
    import simpleimages

    class YourModel(models.Model):
        image = models.ImageField(
            upload_to='images/'
        )
        thumbnail_image = models.ImageField(
            blank=True,
            null=True,
            editable=False,
            upload_to='transformed_images/thumbnails/'
        )
        large_image = models.ImageField(
            blank=True,
            null=True,
            editable=False,
            upload_to='transformed_images/large/'
        )

        transformed_fields = {
            'image': {
                'thumbnail_image': simpleimages.transforms.scale(width=10),
                'large_image': simpleimages.transforms.scale(width=200),
            }
        }

    simpleimages.tracking.track_model(YourModel)

:py:func:`~.tracking.track_model` is called with the model you want to
track. When that model is saved,
:py:func:`~.utils.perform_transformation` uses the ``transformed_fields``
attribute of the model to determine a mapping of source to destination
and transform functions.

See :py:mod:`.transforms` for all the provided transformations.

.. _dimension_caching:

Dimension Caching
^^^^^^^^^^^^^^^^^

I would recommend using
:py:attr:`~django.db.models.ImageField.height_field` and
:py:attr:`~django.db.models.ImageField.width_field` to save the image
dimensions. Otherwise (at least with
:py:class:`storages.backends.s3boto.S3BotoStorage`), the file will have
to be retrieved once to get :py:attr:`~django.db.models.fields.files.FieldFile.url`
and another time to get the dimensions::

    import os

    from django.db import models

    import simpleimages
    import dumper


    class Photo(models.Model):
        def image_path_function(subfolder):
            return lambda instance, filename: os.path.join(
                'photos',
                subfolder,
                filename
            )

        image = models.ImageField(
            upload_to=image_path_function('original'),
            max_length=1000,

        )
        thumbnail_image = models.ImageField(
            blank=True,
            null=True,
            editable=False,
            upload_to=image_path_function('thumbnail'),
            height_field='thumbnail_image_height',
            width_field='thumbnail_image_width',
            max_length=1000
        )
        large_image = models.ImageField(
            blank=True,
            null=True,
            editable=False,
            upload_to=image_path_function('large'),
            height_field='large_image_height',
            width_field='large_image_width',
            max_length=1000
        )
        # cached dimension fields
        thumbnail_image_height = models.PositiveIntegerField(
            null=True,
            blank=True,
            editable=False,
        )
        thumbnail_image_width = models.PositiveIntegerField(
            null=True,
            blank=True,
            editable=False,
        )
        large_image_height = models.PositiveIntegerField(
            null=True,
            blank=True,
            editable=False,
        )
        large_image_width = models.PositiveIntegerField(
            null=True,
            blank=True,
            editable=False,
        )

        transformed_fields = {
            'image': {
                'thumbnail_image': simpleimages.transforms.scale(height=600),
                'large_image': simpleimages.transforms.scale(height=800),
            }
        }

    simpleimages.trackers.track_model(Photo)



Management Command
------------------

Since the images are only transformed on the save of the model, if you
change the transform function, the instances will not be updated until
you resave them. If you want to retransform all the images in a model or
app use :py:mod:`.management.commands.retransform`
