django-simpleimages
===================

.. image:: https://travis-ci.org/saulshanabrook/django-simpleimages.png
    :target: https://travis-ci.org/saulshanabrook/django-simpleimages

.. image:: https://coveralls.io/repos/saulshanabrook/django-simpleimages/badge.png?branch=master
    :target: https://coveralls.io/r/saulshanabrook/django-simpleimages


``django-simpleimages`` is an opinionated Django app which makes it very simple to
deal transforming images on models, with extremely minimal configuration, as long as:

* You want to define sizes in the model and not dynamically in the template
* You provide your own storage backend
* You want the transformation to happen when the model saves

If any of the above don't hold true, then this library probably won't work for
you.  That said, if all of the above do hold true for you, then this app will
likely be the simplest and best way to apply tranformations to images.


Installation
------------

Installation is as easy as::

    pip install django-simpleimages
    pip install pillow # or any other version of PIL

Note: ``django-simpleimages`` requires Django>=1.5 because it needs to use
the ``update_fields`` argument for model saving, which was implemented in 1.5.

Then add ``simpleimages`` to your ``INSTALLED_APPS``.


Usage
---------------

models.py
^^^^^^^^^^^
Here is an example model that will create transformed images on save.

.. code-block:: python

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

    simpleimages.track_model(YourModel)

``simpleimages.track_model`` is called with the model to track.


The model should have a field called ``transformed_fields`` which is a
dictionary mapping original image fields to transformed fields.
Each of the original image keys maps to a dictionary which maps transformed
fields to transformations. The transformations are function that
take an image, from the ``file`` attribute of the original field, and return a
transformed instance of `django.core.files.File
<https://docs.djangoproject.com/en/dev/ref/files/file/#django.core.files.File>`_,
not Python's built-in file object.

Management Command
^^^^^^^^^^^^^^^^^^^

Since the images are only transformed on the save of the model, if you change
a transform, all the models will not be updated until you resave them.
If you want to retransform all the images in a model or app use the
``retransform`` command.

.. code-block:: bash

    # re-transforms and saves all models. If an app is specified then only
    # the models in that app will be re transformed. If a model is specified
    # then only that model in that app will be retransformed. If a field is
    # specified within that model, then that field will be recalculated.
    # If the field is a transformed field, then it will resave that transformed
    # field. If it is a regular field, it will save all the transformations
    # for that field.
    python manage.py retransform app.model.[field]


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

    pip install -e .
    pip install -r requirements-dev.txt
    coverage run --branch --source=simpleimages -m django-mini -a simpleimages -a simpleimages.test --test-runner 'discover_runner.DiscoverRunner' test

Check if the README.rst looks right::

    restview -e 'python setup.py --long-description'

Then push the finished feature to github and open a pull request form the branch.

New Release
^^^^^^^^^^^
To create a new release:

1. Add changes to ``CHANGES.txt``
2. Change version in ``setup.py``
3. ``python setup.py register``
4. ``python setup.py sdist upload``
