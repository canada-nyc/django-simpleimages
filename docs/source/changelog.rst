=========
Changelog
=========
* :release:`1.3.4 <2017.06.06>`
* :bug:`-` Save color profiles with images
* :release:`1.3.3 <2015.12.26>`
* :bug:`-` Fixed Celery task defination.
* :release:`1.3.2 <2015.12.22>`
* :support:`26` Removed lambdas in docs for model.
* :bug:`-` Removed extranious `print` debugging.
* :release:`1.3.1 <2015.12.16>`
* :feature:`-` Added support for Django 1.9.
* :release:`1.3.0 <2015.11.08>`
* :feature:`-` Remove support for PQ (it isn't being maintained).
* :feature:`-` Added support for Celery.
* :feature:`-` Added support for Python 3.5 and Django 1.7, 1.8.
* :support:`-` Changed to use Docker for development.
* :release:`1.2.0 <2014.04.07>`
* :support:`19` Change to use Releases for changelog.
* :feature:`16` Support Django 1.7 (experimental).
* :bug:`15 major` Make compatible with ``height_field`` and ``width_field``.
* :support:`13` Add testing for 3rd party transformation support.
* :release:`1.1.1 <2014.01.27>`
* :bug:`-` Fix height/width order. Before they were reversed and broken.
* :release:`1.1.0 <2014.01.14>`
* :support:`-` Display progress for management command.
* :feature:`-` Require Pillow.
* :release:`1.0.5 <2013.09.04>`
* :bug:`-` Check if destination field exists before deleting.
* :release:`1.0.4 <2013.09.04>`
* :feature:`-` Deletion of destination field when no source exists or transformation fails.
* :release:`1.0.3 <2013.09.02>`
* :support:`-` Fixed spelling for caller setting.
* :release:`1.0.2 <2013.08.31>`
* :bug:`-` Fixed adding management command directory
* :release:`1.0.1 <2013.08.31>`
* :bug:`-` Added management directory to packages so that Django finds command
* :release:`1.0.0 <2013.08.23>`
* :support:`-` Added Sphinx docs.
* :support:`-` Use py.test for testing.
* :feature:`-` Added option to django-rq
* :release:`0.2.8 <2013.07.10>`
* :feature:`-` Added option to not overwrite image.
* :release:`0.2.7 <2013.06.06>`
* :bug:`-` Save only filename and not whole path for transformed images.
* :release:`0.2.6 <2013.06.06>`
* :bug:`-` Use .count() for management command instead of len()
* :release:`0.2.5 <2013.06.04>`
* :bug:`-` Fixed ``retransform`` with no fields.
* :release:`0.2.4 <2013.06.04>`
* :support:`-` Increased transform debug logging.
* :release:`0.2.3 <2013.06.04>`
* :bug:`-` Add all packages so that Django finds management command
* :release:`0.2.2 <2013.06.04>`
* :bug:`-` Zip safe on setup.py so Django finds management command.
* :release:`0.2.1 <2013.05.29>`
* :feature:`-` Reimplement progressive and optimize support.
* :release:`0.2.0 <2013.05.29>`
* :feature:`20` Don't save image with optimize either, because encoutner error.
* :release:`0.1.9 <2013.05.29>`
* :bug:`-` Don't save image as progressive, because encounters error.
* :release:`0.1.8 <2013.05.29>`
* :bug:`-` Convert image to JPEG colorspace.
* :feature:`-` Save image as progressive.
* :feature:`-` Save image with higher quality.
* :release:`0.1.7 <2013.05.29>`
* :bug:`-` Transform post save.
* :bug:`-` Addressed force_update error.
* :release:`0.1.6 <2013.05.29>`
* :support:`-` Reasons why to use library added to readme.
* :bug:`-` Moved error handling to transform function.
* :release:`0.1.5 <2013.04.18>`
* :bug:`-` Make sure image exists before trying to delete it.
* :release:`0.1.4 <2013.04.18>`
* :feature:`-` Support uploading of non-image files.
* :release:`0.1.3 <2013.03.20>`
* :support:`-` Added instructions to add to ``INSTALLED_APPS``.
* :release:`0.1.2 <2013.03.20>`
* :support:`-` Added requirement for at least Django 1.5.
* :release:`0.1.1 <2013.03.20>`
* :support:`-` Fixed Readme formatting.
* :release:`0.1.0 <2013.03.19>`
* :feature:`-` Basic functionality.
