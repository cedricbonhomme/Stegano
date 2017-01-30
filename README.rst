Stéganô
=======

.. image:: https://img.shields.io/pypi/v/Stegano.svg
    :target: https://pypi.python.org/pypi/Stegano

.. image:: https://img.shields.io/pypi/l/Stegano.svg
    :target: https://pypi.python.org/pypi/Stegano

.. image:: https://api.travis-ci.org/cedricbonhomme/Stegano.svg?branch=master
    :target: https://travis-ci.org/cedricbonhomme/Stegano

.. image:: https://img.shields.io/badge/SayThanks.io-%E2%98%BC-1EAEDB.svg
    :target: https://saythanks.io/to/cedricbonhomme


`Stéganô <https://github.com/cedricbonhomme/Stegano>`_, a pure Python
Steganography module.


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


Use Stéganô as a program
''''''''''''''''''''''''

Hide a message
~~~~~~~~~~~~~~


.. code:: bash

    $ lsb hide -i ./tests/sample-files/Lenna.png -m "Secret Message" -o Lena1.png


Hide the message with the Sieve of Eratosthenes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: bash

    $ lsb-set hide -i ./tests/sample-files/Lenna.png -m 'Secret Message' --generator eratosthenes -o Lena2.png

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
