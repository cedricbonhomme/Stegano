.. Stéganô documentation master file, created by
   sphinx-quickstart on Wed Jul 25 13:33:39 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Presentation
============

.. image:: https://builds.sr.ht/~cedric/stegano.svg
    :target: https://builds.sr.ht/~cedric/stegano


Stegano_ is a pure Python steganography_ module.

Steganography is the art and science of writing hidden messages in such a way
that no one, apart from the sender and intended recipient, suspects the
existence of the message, a form of security through obscurity.
Consequently, functions provided by Stegano only hide messages,
without encryption. Steganography is often used with cryptography.

Stegano implements these methods of hiding:

- using the red portion of a pixel to hide ASCII messages;
- using the `Least Significant Bit <http://en.wikipedia.org/wiki/Least_significant_bit>`_ (LSB) technique;
- using the LSB technique with sets based on generators (Sieve for Eratosthenes, Fermat, Mersenne numbers, etc.);
- using the description field of the image (JPEG and TIFF).

Moreover some methods of steganalysis_ are provided:

- steganalysis of LSB encoding in color images;
- statistical steganalysis.

You can also use Stegano through a `Web service <https://github.com/cedricbonhomme/stegano-web>`_.
Not all functionalities of Stegano are covered.

Requirements
============

- Python_ 3;
- `Pillow`_;
- `piexif`_.


Tutorial
========

.. toctree::
    :maxdepth: 2

    installation
    module
    software
    steganalysis

You can have a look at the
`unit tests <https://git.sr.ht/~cedric/stegano/tree/master/tests>`_.


License
=======

Stegano_ is under GPL v3 license.


Donation
========

If you wish and if you like Stegano, you can
`donate <https://github.com/sponsors/cedricbonhomme>`_.



Contact
=======

`My home page <https://www.cedricbonhomme.org>`_


.. _Python: https://www.python.org
.. _Stegano: https://sr.ht/~cedric/stegano
.. _`Pillow`: https://pypi.python.org/pypi/Pillow
.. _`piexif`: https://pypi.python.org/pypi/piexif
.. _steganography: http://en.wikipedia.org/wiki/Steganography
.. _steganalysis: http://en.wikipedia.org/wiki/Steganalysis
