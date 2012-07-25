Getting Stéganô
===============

.. code-block:: bash

    $ hg clone https://bitbucket.org/cedricbonhomme/stegano
    $ cd stegano/
    $ chmod u+x *.py # if you want to use Stéganô in command line

Installation
============

.. code-block:: bash

    $ python setup.py install

Now you will be able to use Stéganô in your Python program.

Using Stéganô as a Python module
================================

.. code-block:: python

    Python 2.7 (r27:82500, Jul  5 2010, 10:14:47)
    [GCC 4.3.2] on linux2
    Type "help", "copyright", "credits" or "license" for more information.
    >>> from stegano import slsb
    >>> secret = slsb.hide("./pictures/Lenna.png", "Hello world!")
    >>> secret.save("./Lenna-secret.png")
    >>> slsb.reveal("./Lenna-secret.png")
    Hello world!

Using Stéganô in command line for your scripts
==============================================

Display help
------------

.. code-block:: bash

    $ ./slsb.py --help
    Usage: slsb.py [options]

    Options:
    --version             show program's version number and exit
    -h, --help            show this help message and exit
    --hide                Hides a message in an image.
    --reveal              Reveals the message hided in an image.
    -i INPUT_IMAGE_FILE, --input=INPUT_IMAGE_FILE
                            Input image file.
    -o OUTPUT_IMAGE_FILE, --output=OUTPUT_IMAGE_FILE
                            Output image containing the secret.
    -m SECRET_MESSAGE, --secret-message=SECRET_MESSAGE
                            Your secret message to hide (non binary).
    -f SECRET_FILE, --secret-file=SECRET_FILE
                            Your secret to hide (Text or any binary file).
    -b SECRET_BINARY, --binary=SECRET_BINARY
                            Output for the binary secret (Text or any binary
                            file).

Hide and reveal a text message
------------------------------

.. code-block:: bash

    $ ./slsb.py --hide -i ./pictures/Lenna.png -o ./pictures/Lenna_enc.png -m HelloWorld!
    $ ./slsb.py --reveal -i ./pictures/Lenna_enc.png
    HelloWorld!

Hide and reveal a binary file
-----------------------------

.. code-block:: bash

    $ wget http://www.gnu.org/music/free-software-song.ogg
    $ ./slsb.py --hide -i ./pictures/Montenach.png -o ./pictures/Montenach_enc.png -f ./free-software-song.ogg
    $ rm free-software-song.ogg
    $ ./slsb.py --reveal -i ./pictures/Montenach_enc.png -b ./song.ogg

Hide and reveal a message by using the description field of the image
---------------------------------------------------------------------

.. code-block:: bash

    $ ./exif-header.py --hide -i ./Elisha-Cuthbert.jpg -o ./Elisha-Cuthbert_enc.jpg -f ./fileToHide.txt
    $ ./exif-header.py --reveal -i ./Elisha-Cuthbert_enc.jpg

Steganalysis
------------

.. code-block:: bash

    $ ./steganalysis-parity.py -i ./pictures./Lenna_enc.png -o ./pictures/Lenna_enc_st.png

 
