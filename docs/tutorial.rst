Installation
============

.. code-block:: bash

    $ sudo pip install Stegano

You will be able to use Stéganô in your Python programs
or as a command line tool.

If you want to retrieve the source code (with the unit tests):

.. code-block:: bash

    $ git clone https://github.com/cedricbonhomme/Stegano.git

.. image:: https://api.travis-ci.org/cedricbonhomme/Stegano.svg?branch=master
    :target: https://travis-ci.org/cedricbonhomme/Stegano

Using Stéganô as a Python module
================================

LSB method
----------

.. code-block:: python

    Python 3.5.1 (default, Dec  7 2015, 11:33:57)
    [GCC 4.9.2] on linux
    Type "help", "copyright", "credits" or "license" for more information.
    >>> from stegano import slsb
    >>> secret = slsb.hide("./examples/pictures/Lenna.png", "Hello world!")
    >>> secret.save("./Lenna-secret.png")
    >>> print(slsb.reveal("./Lenna-secret.png"))
    Hello world!

Description field of the image
------------------------------

For JPEG and TIFF images.

.. code-block:: python

    Python 3.5.1 (default, Dec  7 2015, 11:33:57)
    [GCC 4.9.2] on linux
    Type "help", "copyright", "credits" or "license" for more information.
    >>> from stegano import exifHeader
    >>> secret = exifHeader.hide("./examples/pictures/20160505T130442.jpg",
                            "./image.jpg", secret_message="Hello world!")
    >>> print(exifHeader.reveal("./image.jpg"))

More examples are available in the
`tests <https://github.com/cedricbonhomme/Stegano/tree/master/tests>`_.

Using Stéganô in command line for your scripts
==============================================

Display help
------------

.. code-block:: bash

    $ slsb --help
    Usage: slsb [options]

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

    $ slsb --hide -i ./pictures/Lenna.png -o ./pictures/Lenna_enc.png -m HelloWorld!
    $ slsb --reveal -i ./pictures/Lenna_enc.png
    HelloWorld!

Hide and reveal a binary file
-----------------------------

.. code-block:: bash

    $ wget http://www.gnu.org/music/free-software-song.ogg
    $ slsb --hide -i ./pictures/Montenach.png -o ./pictures/Montenach_enc.png -f ./free-software-song.ogg
    $ rm free-software-song.ogg
    $ slsb --reveal -i ./pictures/Montenach_enc.png -b ./song.ogg

Hide and reveal a message by using the description field of the image
---------------------------------------------------------------------

.. code-block:: bash

    $ ./exif-header.py --hide -i ./Elisha-Cuthbert.jpg -o ./Elisha-Cuthbert_enc.jpg -f ./fileToHide.txt
    $ ./exif-header.py --reveal -i ./Elisha-Cuthbert_enc.jpg

Steganalysis
------------

.. code-block:: bash

    $ steganalysis-parity -i ./pictures./Lenna_enc.png -o ./pictures/Lenna_enc_st.png
