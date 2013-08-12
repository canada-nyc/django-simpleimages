Why...?
=======

I believe that keeping the implementation of this package as simple as
possible. When I say simple, I mean in comparison to other image
transformation packages in Django.


The Alternative
-----------------
.. highlight:: html+django

The most popular apps, such as sorl-thumbnail_, generate the transformed
images in the request-response cycle, in the template or the views. That
was the images are never out of date and are not stored in the database,
which makes sense because there isn't really anything new that should be
stored by a scaled down image. And it makes sense that it is present in
the template, because it really is a presentation detail. And it is the
easiest method, and can be implemented with a few lines of code. For
example::

    {% thumbnail item.image "100x100" crop="center" as im %}
        <img src="{{ im.url }}" width="{{ im.width }}" height="{{ im.height }}">
    {% endthumbnail %}

Performance Problems
^^^^^^^^^^^^^^^^^^^^
I ran into performance problems with this approach. Since images are
generated in the request-response cycle, caching strategies are essential
to minimize database and storage access. I then found django-imagekit_,
which is much more advanced and allows a great flexibility on every bit
of the image generation process. However I still found myself
struggling to understand the exact implementation details of how and
when the images were generated. This isn't something I should have been
worrying about, apart from the fact that some of my pages were timing
out generating hundreds of thumbnails.


My Solution
-----------
So I decided to write an implementation that anyone could understand.
``django-simpleimages`` uses the standard
Even though is more verbose, and requires an extra database column,
storing transformed images in their own fields presents several
advantages. It allows
:ref:`caching of image dimensions <dimension_caching>`, using
Django's built in solution. It also is easy to understand when the
storage backend is being accessed, because you are simply accessing a
normal :py:class:`~django.db.models.ImageField`.


.. _sorl-thumbnail: https://github.com/sorl/sorl-thumbnail
.. _django-imagekit: https://github.com/jdriscoll/django-imagekit
