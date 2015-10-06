Stéganô
=======

A Python Steganography module.


Installation
------------

    $ sudo pip install Stegano


Use Stéganô as a library in your Python program
-----------------------------------------------

If you want to use Stéganô in your Python program you just have to import the
appropriate steganography technique. For example:


    >>> from stegano import slsb
    >>> secret = slsb.hide("./pictures/Lenna.png", "Hello Workd")
    >>> secret.save("./Lenna-secret.png")


Use Stéganô as a program
------------------------

In addition you can use Stéganô as a program.

Example:

    $ slsb --hide -i ../examples/pictures/Lenna.png -o Lena1.png -m "Secret Message"

Another example (hide the message  with Sieve of Eratosthenes):

    $ slsb-set --hide -i ../examples/pictures/Lenna.png -o Lena2.png --generator eratosthenes -m 'Secret Message'


Examples
--------

There are some examples in the folder *examples*.

    $ hg clone https://bitbucket.org/cedricbonhomme/stegano
    $ cd stegano/examples


Turorial
--------

A [tutorial](https://stegano.readthedocs.org/en/latest/tutorial) is available.


Contact
-------

[My home page](https://www.cedricbonhomme.org).
