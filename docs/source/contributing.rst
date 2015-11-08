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

To run the tests::

    docker-compose up -d db redis
    docker-compose run tests

Compile the documentation and check if it looks right::

    docker-compose run tests make docs-html
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
