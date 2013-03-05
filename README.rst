django-simpleimages
==================

.. image:: https://travis-ci.org/saulshanabrook/django-simpleimages.png
    :target: https://travis-ci.org/saulshanabrook/django-simpleimages

``django-simpleimages` is an opinionated Django app which makes it very simple to
deal transforming images on models, with extremely minimal configuration, as long as:

* You want to define transformations in the model, and not in the template
* You want have your own storage backend
* You want the tranformation to happen when the model saves

If any of the above don't hold true, then this library probably won't work for
you.  That said, if all of the above do hold true for you, then this app will
likely be the simplest and best way to apply tranformations to images.


Installation
------------

Installation is as easy as::

    pip install django-simpleimages

Done!

Configuration
-------------

settings.py
^^^^^^^^^^^

``django-simpleimages`` will use the ``DEFAULT_FILE_STORAGE``::

    # If you don't want this to be the global default, just make sure you
    # specify the an alternative backend.
    DEFAULT_FILE_STORAGE = 'other.storage.backend'

Usage
---------------

models.py
^^^^^^^^^^^
Here is an example model with a image tranform field.

::
    import os

    from django.db import models
    import simpleimages

    class YourModel(models.Model)
        def large_upload_to(original_file_path):
            path, extension = os.path.splitext(original_file_path)
            return path + '_large_file' + extension

        image = simpleimages.fields.ImageTransformField(
            upload_to="store/product_images",
            thumbs={
                'thumb': (
                    simpleimages.utils.append_to_filename('_thumb'),
                    simpleimages.transforms.scale(width=20, height=20),
                )
                'large': (
                    large_upload_to,
                    simpleimages.transforms.scale(width=200),
                )
            }
        )

The values in the `thumbs` dictionary tuples that hold two functions. The
first takes the file path of the original image as its first argument and
returns the modified path. The second takes the original image as its first
argument and returns the modifed image to be saved.

Accessing the Files
^^^^^^^^^^^

::
    YourModel.image # original image, a Django File object
    YourModel.image.thumbs # Dictionary of thumbs
    YourModel.image.thumbs['large'] # modified image, Django File object
    YourModel.image.thumbs['large'].path # Path saved
    YourModel.image.thumbs['large'].url # Absolute url


Contributing
------------

If you find issues or would like to see a feature suppored, head over to
the `issues section:
<https://github.com/saulshanabrook/django-simpleimages/issues>`_ and report it.

To contribute code in any form, fork the `github repository:
<https://github.com/saulshanabrook/django-simpleimages>`_ and clone it locally.
Create a new branch for your feature::

    git commit -b feature/whatever-you-like

Then make sure all the tests past (and write new ones for any new features)::
    pip install -r requirements-dev.txt
    pip install -e .
    django-mini.py -a simpleimages --test-runner 'discover_runner.DiscoverRunner' test


Then push the finished feature to github and open a pull request form the branch.
