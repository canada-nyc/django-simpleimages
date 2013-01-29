=========
Changelog
=========

0.1.3
-----

* Increased the max length of the old and new URL database fields to match
  Django's redirects app (200).

0.1.2
-----

* The middleware now supports URLs that contain a query string and
  redirect using 301 or 410 as with other URLs now. That means it
  is possible to redirect ``/some/old/url/using.php?with=query&in=string``
  to a shiny new URL.


0.1.1
-----

* Initial release of the package
