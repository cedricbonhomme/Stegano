Stéganô
=======

.. image:: https://img.shields.io/pypi/pyversions/Stegano.svg?style=flat-square
    :target: https://pypi.python.org/pypi/Stegano

.. image:: https://img.shields.io/pypi/v/Stegano.svg?style=flat-square
    :target: https://github.com/cedricbonhomme/Stegano/releases/latest

.. image:: https://img.shields.io/pypi/l/Stegano.svg?style=flat-square
    :target: https://www.gnu.org/licenses/gpl-3.0.html

.. image:: https://img.shields.io/travis/cedricbonhomme/Stegano/master.svg?style=flat-square
    :target: https://travis-ci.org/cedricbonhomme/Stegano

.. image:: https://img.shields.io/coveralls/cedricbonhomme/Stegano/master.svg?style=flat-square
   :target: https://coveralls.io/github/cedricbonhomme/Stegano?branch=master

.. image:: https://img.shields.io/github/stars/cedricbonhomme/Stegano.svg?style=flat-square
    :target: https://github.com/cedricbonhomme/Stegano/stargazers

.. image:: https://img.shields.io/badge/SayThanks.io-%E2%98%BC-1EAEDB.svg?style=flat-square
    :target: https://saythanks.io/to/cedricbonhomme


`Stéganô <https://github.com/cedricbonhomme/Stegano>`_, a pure Python
Steganography module.

Steganography is the art and science of writing hidden messages in such a way
that no one, apart from the sender and intended recipient, suspects the
existence of the message, a form of security through obscurity. Consequently,
functions provided by Stéganô only hide messages, without encryption.
Steganography is often used with cryptography.

Installation
------------

.. code:: bash

    $ sudo pip install Stegano

You will be able to use Stéganô in your Python programs or as a command line
tool.


Usage
-----

A `tutorial <https://stegano.readthedocs.io>`_ is available.


Use Stéganô as a library in your Python program
'''''''''''''''''''''''''''''''''''''''''''''''

If you want to use Stéganô in your Python program you just have to import the
appropriate steganography technique. For example:

.. code:: python

    >>> from stegano import lsb
    >>> secret = lsb.hide("./tests/sample-files/Lenna.png", "Hello World")
    >>> secret.save("./Lenna-secret.png")
    >>>
    >>> clear_message = lsb.reveal("./Lenna-secret.png")


Use Stéganô as a program
''''''''''''''''''''''''

Hide a message
~~~~~~~~~~~~~~


.. code:: bash

    $ stegano-lsb hide -i ./tests/sample-files/Lenna.png -m "Secret Message" -o Lena1.png

Reveal the message
~~~~~~~~~~~~~~~~~~

.. code:: bash

    $ stegano-lsb reveal -i Lena1.png
    Secret Message


Hide the message with the Sieve of Eratosthenes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: bash

    $ stegano-lsb-set hide -i ./tests/sample-files/Lenna.png -m 'Secret Message' --generator eratosthenes -o Lena2.png

The message will be scattered in the picture, following a set described by the
Sieve of Eratosthenes. Other sets are available. You can also use your own
generators.

This will make a steganalysis more complicated.


Running the tests
-----------------

.. code:: bash

    $ python -m unittest discover -v


Contact
-------

`Cédric Bonhomme <https://www.cedricbonhomme.org>`_
