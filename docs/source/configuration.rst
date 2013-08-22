Configuration
===============================================

Add ``simpleimages`` to your ``INSTALLED_APPS`` to use the
management command.

If you want to transform the images uses workers, set the
``SIMPLEIMAGES_TRANFORM_CALLER`` to a function that will call
the transform function. It defaults to ``'simpleimages.callers.default'``

See :ref:`async docs<async>` for details.


Requirements
------------
* Django > 1.5
* Python 2.7, 3.2, 3.3
