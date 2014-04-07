Contributing
============

If you find issues or would like to see a feature suppored, head over to
the `issues section:
<https://github.com/saulshanabrook/django-simpleimages/issues>`_ and report it.

To contribute code in any form, fork the `github repository:
<https://github.com/saulshanabrook/django-simpleimages>`_ and clone it locally.
Create a new branch for your feature::

    git commit -b feature/whatever-you-like

Add proper docstrings to any changed or added code.

Then make sure all the tests past (and write new ones for any new features).

To run the tests you must be running PostgreSQL with a database
called ``django_simpleimages_test``. To create one run::

    createuser -s postgres
    psql -c 'create database django_simpleimages;' -U postgres

Then install Python dependencies::

    pip install -e .
    pip install -r requirements-dev.txt


And finally run the tests::

    py.test

To test for RQ support, you must have a Redis installed and accesible
via default login. If py.test can't find a working Redis connection,
it will skip the RQ tests.

Check if the ``README.rst`` looks right::

    restview --long-description

Compile the documentation and check if it looks right::

    make docs-html
    open docs/build/index.html

Then push the finished feature to github and open a pull request form the branch.

New Release
-----------
To create a new release:

1. Add changes to ``docs/source/changelog.rst``, using Releases_ formatting
2. Change version in ``setup.py``
3. Change version in ``docs/source/conf.py``
4. ``python setup.py sdist upload``
5. ``python setup.py bdist_wheel``
6. ``git tag x.x.x``
7. Push git tag and commit
8. Add release to github tag, with changes and releasion name.

.. _releases: http://releases.readthedocs.org/en/latest/concepts.html
