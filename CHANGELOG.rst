Release History
===============

0.5.2 (2016-05-18)
------------------

* improvements and bug fixes for the exifHeader module;
* added unit tests for the exifHeader module;
* improvements of the documentation.

0.5.1 (2016-04-16)
------------------

* minor improvements and bug fixes;
* added unit tests for the slsb and slsbset modules.

0.5 (2016-03-18)
----------------

* management of greyscale images.

0.4.6 (2016-03-12)
------------------

* bugfix when the length of the message to hide is not divisible by 3,
  for the slsb and slsbset module.

0.4.5 (2015-12-23)
------------------
* bugfix.

0.4.4 (2015-12-23)
------------------

* new project home page;
* minor updated to the documentation.

0.4.3 (2015-10-06)
------------------

* bug fixes for Python 3;
* bug fixes in the scripts in *./bin*.

0.4.2 (2015-10-05)
------------------

* first stable release on PypI.

0.4 (2012-01-02)
----------------

This release introduces a more advanced LSB (Least Significant Bit) method
based on integers sets. The sets generated with Python generators
(Sieve of Eratosthenes, Fermat, Carmichael numbers, etc.) are used to select
the pixels used to hide the information. You can use these new methods in your
Python codes as a Python module or as a program in your scripts.

0.3 (2011-04-15)
----------------

* you can now use Stéganô as a library in your Python program;
  (python setup.py install) or as a 'program' thanks to the scripts provided
  in the bin directory;
* new documentation (reStructuredText) comes with Stéganô.

0.2 (2011-03-24)
----------------

* this release introduces some bugfixes and a major speed improvement of the
  *reveal* function for the LSB method. Moreover it is now possible to hide a
  binary file (ogg, executable, etc.);
* a new technique for hiding/revealing a message in a JPEG picture by using the
  description field of the image is provided.
