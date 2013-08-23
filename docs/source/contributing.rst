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

Then make sure all the tests past (and write new ones for any new features)::

    pip install -e .
    pip install -r requirements-dev.txt
    py.test

Check if the ``README.rst`` looks right::

    restview --long-description

Compile the documentation and check if it looks right::

    make docs-html
    open docs/build/index.html

Then push the finished feature to github and open a pull request form the branch.

New Release
-----------
To create a new release:

1. Add changes to ``CHANGES.txt``
2. Change version in ``setup.py``
3. Change version in ``docs/source/conf.py``
4. ``python setup.py register``
5. ``python setup.py sdist upload``
