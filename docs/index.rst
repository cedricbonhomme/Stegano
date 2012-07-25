.. Stéganô documentation master file, created by
   sphinx-quickstart on Wed Jul 25 13:33:39 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Stéganô's documentation!
===================================

.. toctree::
   :maxdepth: 2

Stéganô is a Python Steganography module.
Steganography is the art and science of writing hidden messages in such a way that no one,
apart from the sender and intended recipient, suspects the existence of the message, a form
of security through obscurity. Consequently, functions provided by Stéganô only hide message,
without encryption. Indeed steganography is often used with cryptography.

The advantage of steganography, over cryptography alone, is that messages do not attract
attention to themselves. If you are interested in cryptography have a look at my project pySecret.

Requirements
============

- Python (2.4 -> 2.7);
- Python Imaging Library (PIL).

Methods of hiding
=================

For the moment, Stéganô implements these methods of hiding:

- using the red portion of a pixel to hide ASCII messages;
- using the Least Significant Bit (LSB) technique;
- using the LSB technique with sets based on generators (Sieve for Eratosthenes, Fermat, Mersenne numbers, etc.);
- using the description field of the image (JPEG).

Moreover some methods of steganalysis are provided:

- steganalysis of LSB encoding in color images;
- statistical steganalysis. 



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

