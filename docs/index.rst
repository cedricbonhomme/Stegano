.. Stéganô documentation master file, created by
   sphinx-quickstart on Wed Jul 25 13:33:39 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Stéganô's documentation!
===================================

.. toctree::
   :maxdepth: 2

Stéganô is a Python steganography_ module.
Steganography is the art and science of writing hidden messages in such a way that no one,
apart from the sender and intended recipient, suspects the existence of the message, a form
of security through obscurity. Consequently, functions provided by Stéganô only hide message,
without encryption. Indeed steganography is often used with cryptography.

The advantage of steganography, over cryptography alone, is that messages do not attract
attention to themselves. If you are interested in cryptography have a look at my project pySecret.


Download Stéganô
================

You can clone the source code of Stéganô_ :

.. code-block:: bash

    $ hg clone https://bitbucket.org/cedricbonhomme/stegano/

More information about how to install Stéganô in the :doc:`tutorial </tutorial>`.

Requirements
============

- Python_ >= 3.2 (tested with Python 3.3.1);
- `Pillow`_ (friendly fork of Python Imaging Library).

Methods of hiding
=================

For the moment, Stéganô implements these methods of hiding:

- using the red portion of a pixel to hide ASCII messages;
- using the `Least Significant Bit <http://en.wikipedia.org/wiki/Least_significant_bit>`_ (LSB) technique;
- using the LSB technique with sets based on generators (Sieve for Eratosthenes, Fermat, Mersenne numbers, etc.);
- using the description field of the image (JPEG).

Moreover some methods of steganalysis_ are provided:

- steganalysis of LSB encoding in color images;
- statistical steganalysis. 


Turorial
========

More information available at the :doc:`tutorial </tutorial>` page

License
=======

Stéganô is under GPL v3 license.

Donation
========

If you wish and if you like Stéganô, you can donate via bitcoin. My bitcoin address: `1GVmhR9fbBeEh7rP1qNq76jWArDdDQ3otZ <http://blockexplorer.com/address/1GVmhR9fbBeEh7rP1qNq76jWArDdDQ3otZ>`_

Contact
=======

`My home page <http://cedricbonhomme.org>`_

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. _Python: http://python.org/
.. _Stéganô: https://bitbucket.org/cedricbonhomme/stegano/
.. _`Pillow`: https://pypi.python.org/pypi/Pillow
.. _steganography: http://en.wikipedia.org/wiki/Steganography
.. _steganalysis: http://en.wikipedia.org/wiki/Steganalysis
