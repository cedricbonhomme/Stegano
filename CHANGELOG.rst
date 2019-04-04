Release History
===============

0.9.2 (2019-04-04)
------------------

* updated Pillow dependency to version 6.0.0 in order to fix a bug when opening
  some PNG files (https://github.com/python-pillow/Pillow/issues/3557).

0.9.1 (2019-03-06)
------------------

* updated Pillow dependency in order to fix a bug when opening some PNG files.

0.9.0 (2018-12-18)
------------------

* added the possibility to shift the encoded bits when using the lsbset module.

0.8.6 (2018-11-05)
------------------

* fixed a potential security issue related to CVE-2018-18074.


0.8.5 (2018-04-18)
------------------

* Fixed an encoding problem which occured on Windows during the installation
  of the module.


0.8.4 (2018-02-28)
------------------

* Stegano is ready for use with pipenv and pipsi.


0.8.3 (2018-02-23)
------------------

* the recommended way to install Stegano is now to use pipenv.


0.8.2 (2017-12-20)
------------------

* Fixed a bug with the new 'encoding' function when using Stegano as a command
  line tool. No default value was set. Default value is UTF-8.


0.8.1 (2017-05-16)
------------------

* it is now possible to specify the encoding (UTF-8 or UTF-32LE) of the message
  to hide/reveal through the command line;
* the help of the command line now displays the available choices for the
  arguments, if it is necessary (list of available encodings, list of available
  generators);
* tests expected results lies now in a dedicated folder;
* a script has been added in order to get proper exit code check for mypy.


0.8 (2017-05-06)
----------------

* updated command line. All commands are now prefixed with *stegano-*;
* improved type hints;
* it is possible to load and save images from and to file objects (BytesIO);
* improved checks when revealing a message with the lsbset module fails.


0.7.1 (2017-05-05)
------------------

* improved generators for the lsb-set module;
* improved tests for the generators;
* improved type hints.


0.7 (2017-05-04)
----------------

* unicode is now supported. By default UTF-8 encoding is used. UTF-32LE can also
  be used to hide non-ASCII characters. UTF-8 (8 bits) is the default choice
  since it is possible to hide longer messages with it.
* improved checks with type hints.


0.6.9 (2017-03-10)
------------------

* introduces some type hints (PEP 484);
* more tests for the generators and for the tools module;
* updated descriptions of generators;
* fixed a bug with a generator that has been previously renamed.


0.6.8 (2017-03-08)
------------------

* bugfix: fixed #12: Error when revealing a hidden binary file in an image.


0.6.7 (2017-02-21)
------------------

* bugfix: added missing dependency in the setup.py file.


0.6.6 (2017-02-20)
------------------

* improved docstrings for the desciption of the generators;
* improved the command which displays the list of generators.


0.6.5 (2017-02-16)
------------------

* added a command to list all available generators for the lsb-set module;
* test when the data image is coming via byte stream, for the lsb module.


0.6.4 (2017-02-06)
------------------

* a command line for the 'red' module has been added;
* bugfix: fixed a bug in the lsb-set command line when the generator wasn't
  specified by the user.


0.6.3 (2017-01-29)
------------------

* Support for transparent PNG images has been added (lsb and lsbset modules).


0.6.2 (2017-01-19)
------------------

* bugfix: solved a bug when the image data is coming via byte streams (ByteIO),
  for the exifHeader hiding method.


0.6.1 (2016-08-25)
------------------

* reorganization of the steganalysis sub-module.


0.6 (2016-08-04)
------------------

* improvements of the command line of Stéganô. The use of Stéganô through the
  command line has slightly changed ('hide' and 'reveal' are now sub-parameters
  of the command line). No changes if you use Stéganô as a module in your
  software. The documentation has been updated accordingly.


0.5.5 (2016-08-03)
------------------

* bugfix: Incorrect padding size in `base642string` in tools.base642binary().


0.5.4 (2016-05-22)
------------------

* the generator provided to the functions lsbset.hide() and lsbset.reveal() is
  now a function. This is more convenient for a user who wants to use a custom
  generator (not in the module lsbset.generators).
* performance improvements for the lsb and lsbset modules.


0.5.3 (2016-05-19)
------------------

* reorganization of all modules. No impact for the users of Stegano.


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
