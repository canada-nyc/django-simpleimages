Usage
=====

Models
---------

Here is an example model that will create transformed images on save::

    from django.db import models
    import simpleimages.transforms
    import simpleimages.trackers

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
                'thumbnail_image': simpleimages.transforms.Scale(width=10),
                'large_image': simpleimages.transforms.Scale(width=200),
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

    import simpleimages.transforms
    import simpleimages.trackers

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
                'thumbnail_image': simpleimages.transforms.Scale(height=600),
                'large_image': simpleimages.transforms.Scale(height=800),
            }
        }

    simpleimages.trackers.track_model(Photo)


.. _async:

Performing Transforms Asynchronously
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

By default all transformations are performed when the model is saved.
If you want to instead perform the transformations asynchronously,
for the obvious performance reasons, you by setting
``SIMPLEIMAGES_TRANFORM_CALLER``. Set this to the dotted
path to any function that will take the transform function as its
first argument and the arguments to call it with as subsequent
arguments and keyword arguments. This format was based around
`django-rq`_. To perform all transforms through django-rq set
``SIMPLEIMAGES_TRANFORM_CALLER='django_rq.enqueue'``.

.. _django-rq: https://github.com/ui/django-rq#putting-jobs-in-the-queue

Then you have to account for the fact that sometimes the transformed
images won't be available in time to render them on the page. If you
want to fall back to the source image, if the transformed image isn't
rendered yet, use something like this:


    import os

    from django.db import models

    import simpleimages.transforms
    import simpleimages.trackers

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
            max_length=1000
        )
        large_image = models.ImageField(
            blank=True,
            null=True,
            editable=False,
            upload_to=image_path_function('large'),
            max_length=1000
        )

        @property
        def safe_thumbnail_image(self):
            return self.thumbnail_image or self.image

        @property
        def safe_large_image(self):
            return self.large_image or self.image


        transformed_fields = {
            'image': {
                'thumbnail_image': simpleimages.transforms.Scale(height=600),
                'large_image': simpleimages.transforms.Scale(height=800),
            }
        }

    simpleimages.trackers.track_model(Photo)

Then access the transformed images with ``instance.safe_thumbnail_image``
instead.


Management Command
------------------

Since the images are only transformed on the save of the model, if you
change the transform function, the instances will not be updated until
you resave them. If you want to retransform all the images in a model or
app use :py:mod:`.management.commands.retransform`
