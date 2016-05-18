Stéganô
=======

.. image:: https://api.travis-ci.org/cedricbonhomme/Stegano.svg?branch=master
    :target: https://travis-ci.org/cedricbonhomme/Stegano

A Python Steganography module.


Installation
------------

.. code:: bash

    $ sudo pip install Stegano

You will be able to use Stéganô in your Python programs or as a command line
tool.


Usage
-----

A `tutorial <https://stegano.readthedocs.io>`_ is available.

There are also some examples in the folder `examples <examples>`_.

Use Stéganô as a library in your Python program
'''''''''''''''''''''''''''''''''''''''''''''''

If you want to use Stéganô in your Python program you just have to import the
appropriate steganography technique. For example:

.. code:: python

    >>> from stegano import slsb
    >>> secret = slsb.hide("./pictures/Lenna.png", "Hello World")
    >>> secret.save("./Lenna-secret.png")


Use Stéganô as a program
''''''''''''''''''''''''

.. code:: bash

    $ slsb --hide -i ../examples/pictures/Lenna.png -o Lena1.png -m "Secret Message"

Hide the message  with Sieve of Eratosthenes:

.. code:: bash

    $ slsb-set --hide -i ../examples/pictures/Lenna.png -o Lena2.png --generator eratosthenes -m 'Secret Message'


Running the tests
-----------------

.. code:: bash

    $ python -m unittest discover -v


Contact
-------

`My home page <https://www.cedricbonhomme.org>`_.
