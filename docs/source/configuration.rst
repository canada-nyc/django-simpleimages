Configuration
===============================================

Add ``simpleimages`` to your ``INSTALLED_APPS`` to use the
management command.

If you want to transform the images using workers, set the
``SIMPLEIMAGES_TRANSFORM_CALLER`` to a function that will call
the transform function. It defaults to ``'simpleimages.callers.default'``,
which transforms images synchronously. See :py:mod:`.callers` for all
provided image transform callers.


The :ref:`async docs<async>` section has more details on managing
image retrieval for async creation.


Requirements
------------
* Django 1.5, 1.6, 1.7, 1.8
* Python 2.7, 3.2, 3.3, 3.4, 3.5
