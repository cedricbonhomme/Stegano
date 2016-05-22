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

Hide and reveal a text message with the LSB method
--------------------------------------------------

.. code-block:: bash

    $ lsb --hide -i ./tests/sample-files/Lenna.png -o ./Lenna_enc.png -m HelloWorld!
    $ lsb --reveal -i ./Lenna_enc.png
    HelloWorld!

Hide and reveal a binary file
-----------------------------

.. code-block:: bash

    $ wget http://www.gnu.org/music/free-software-song.ogg
    $ lsb --hide -i ./tests/sample-files/Montenach.png -o ./Montenach_enc.png -f ./free-software-song.ogg
    $ rm free-software-song.ogg
    $ lsb --reveal -i ./Montenach_enc.png -b ./song.ogg

Hide and reveal a text message with the LSB method and generated sets
---------------------------------------------------------------------

Sets are used in order to select the pixels where the message will be hidden.

.. code-block:: bash

    echo "Hide the message  with the Sieve of Eratosthenes..."
    lsb-set --hide -i ./tests/sample-files/Montenach.png -o ./surprise.png --generator eratosthenes -m 'Joyeux Noël!'
    echo ""

    echo "Try to reveal with Mersenne numbers..."
    lsb-set --reveal --generator mersenne -i ./surprise.png
    echo ""

    echo "Try to reveal with fermat numbers..."
    lsb-set --reveal --generator fermat -i ./surprise.png
    echo ""

    echo "Try to reveal with carmichael numbers..."
    lsb-set --reveal --generator carmichael -i ./surprise.png
    echo ""

    echo "Try to reveal with Sieve of Eratosthenes..."
    lsb-set --reveal --generator eratosthenes -i ./surprise.png


An other example:

.. code-block:: bash

    # Hide the message - LSB with a set defined by the identity function (f(x) = x).
    lsb-set --hide -i ./tests/sample-files/Montenach.png -o ./enc-identity.png --generator identity -m 'I like steganography.'

    # Hide the message - LSB only.
    lsb --hide -i ./tests/sample-files/Montenach.png -o ./enc.png -m 'I like steganography.'

    # Check if the two generated files are the same.
    sha1sum ./enc-identity.png ./enc.png

    # The output of lsb is given to lsb-set.
    lsb-set --reveal -i ./enc.png --generator identity

    # The output of lsb-set is given to lsb.
    lsb --reveal -i ./enc-identity.png
