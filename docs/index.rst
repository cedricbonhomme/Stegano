.. Stéganô documentation master file, created by
   sphinx-quickstart on Wed Jul 25 13:33:39 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Stéganô's documentation!
===================================

Presentation
============

Stéganô_ is a Python steganography_ module.

Steganography is the art and science of writing hidden messages in such a way
that no one, apart from the sender and intended recipient, suspects the
existence of the message, a form of security through obscurity.
Consequently, functions provided by Stéganô only hide messages,
without encryption. Steganography is often used with cryptography.

Stéganô implements these methods of hiding:

- using the red portion of a pixel to hide ASCII messages;
- using the `Least Significant Bit <http://en.wikipedia.org/wiki/Least_significant_bit>`_ (LSB) technique;
- using the LSB technique with sets based on generators (Sieve for Eratosthenes, Fermat, Mersenne numbers, etc.);
- using the description field of the image (JPEG and TIFF).

Moreover some methods of steganalysis_ are provided:

- steganalysis of LSB encoding in color images;
- statistical steganalysis.


Requirements
============

- Python_ >= 3.2 (tested with Python 3.5.1);
- `Pillow`_;
- `piexif`_.


Turorial
========

.. toctree::
    :maxdepth: 2

    tutorial

You can also have a look at the
`unit tests <https://github.com/cedricbonhomme/Stegano/tree/master/tests>`_.


License
=======

Stéganô_ is under GPL v3 license.


Donation
========

If you wish and if you like Stéganô, you can donate via bitcoin.
My bitcoin address: `1GVmhR9fbBeEh7rP1qNq76jWArDdDQ3otZ <http://blockexplorer.com/address/1GVmhR9fbBeEh7rP1qNq76jWArDdDQ3otZ>`_


Contact
=======

`My home page <https://www.cedricbonhomme.org>`_


.. _Python: https://www.python.org
.. _Stéganô: https://github.com/cedricbonhomme/Stegano
.. _`Pillow`: https://pypi.python.org/pypi/Pillow
.. _`piexif`: https://pypi.python.org/pypi/piexif
.. _steganography: http://en.wikipedia.org/wiki/Steganography
.. _steganalysis: http://en.wikipedia.org/wiki/Steganalysis
