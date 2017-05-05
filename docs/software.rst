Using Stéganô in command line for your scripts
==============================================

Display help
------------

.. code-block:: bash

    $ stegano-lsb --help
    usage: stegano-lsb [-h] {hide,reveal} ...

    positional arguments:
      {hide,reveal}  sub-command help
        hide         hide help
        reveal       reveal help

    optional arguments:
      -h, --help     show this help message and exit


.. code-block:: bash

    $ stegano-lsb hide --help
    usage: stegano-lsb hide [-h] -i INPUT_IMAGE_FILE (-m SECRET_MESSAGE | -f SECRET_FILE)
                    -o OUTPUT_IMAGE_FILE

    optional arguments:
      -h, --help            show this help message and exit
      -i INPUT_IMAGE_FILE, --input INPUT_IMAGE_FILE
                            Input image file.
      -m SECRET_MESSAGE     Your secret message to hide (non binary).
      -f SECRET_FILE        Your secret to hide (Text or any binary file).
      -o OUTPUT_IMAGE_FILE, --output OUTPUT_IMAGE_FILE
                            Output image containing the secret.


.. code-block:: bash

    $ stegano-lsb reveal --help
    usage: stegano-lsb reveal [-h] -i INPUT_IMAGE_FILE [-o SECRET_BINARY]

    optional arguments:
      -h, --help            show this help message and exit
      -i INPUT_IMAGE_FILE, --input INPUT_IMAGE_FILE
                            Input image file.
      -o SECRET_BINARY      Output for the binary secret (Text or any binary
                            file)


Hide and reveal a text message with the LSB method
--------------------------------------------------

.. code-block:: bash

    $ stegano-lsb hide -i ./tests/sample-files/Lenna.png -m 'Hello World!' -o ./Lenna_enc.png
    $ stegano-lsb reveal -i ./Lenna_enc.png
    Hello World!

Hide and reveal a binary file
-----------------------------

.. code-block:: bash

    $ wget http://www.gnu.org/music/free-software-song.ogg
    $ stegano-lsb hide -i ./tests/sample-files/Montenach.png -f ./free-software-song.ogg -o ./Montenach_enc.png
    $ rm free-software-song.ogg
    $ stegano-lsb reveal -i ./Montenach_enc.png -o ./song.ogg

Hide and reveal a text message with the LSB method and generated sets
---------------------------------------------------------------------

Sets are used in order to select the pixels where the message will be hidden.

.. code-block:: bash

    # Hide the message with the Sieve of Eratosthenes
    $ stegano-lsb-set hide -i ./tests/sample-files/Montenach.png --generator eratosthenes -m 'Joyeux Noël!' -o ./surprise.png

    # Try to reveal with Mersenne numbers
    $ stegano-lsb-set reveal --generator mersenne -i ./surprise.png

    # Try to reveal with fermat numbers
    $ stegano-lsb-set reveal --generator fermat -i ./surprise.png

    # Try to reveal with carmichael numbers
    $ stegano-lsb-set reveal --generator carmichael -i ./surprise.png

    # Try to reveal with Sieve of Eratosthenes
    $ stegano-lsb-set reveal --generator eratosthenes -i ./surprise.png

    # List all available generators
    $ stegano-lsb-set list-generators
    Generator id:
        ackermann
    Desciption:
        Ackermann number.

    Generator id:
        carmichael
    Desciption:
        Composite numbers n such that a^(n-1) == 1 (mod n) for every a coprime to n.
        https://oeis.org/A002997

    Generator id:
        composite
    Desciption:
        Generate the composite numbers using the sieve of Eratosthenes.
        https://oeis.org/A002808

    Generator id:
        eratosthenes
    Desciption:
        Generate the prime numbers with the sieve of Eratosthenes.
        https://oeis.org/A000040

    Generator id:
        fermat
    Desciption:
        Generate the n-th Fermat Number.
        https://oeis.org/A000215

    Generator id:
        fibonacci
    Desciption:
        Generate the sequence of Fibonacci.
        https://oeis.org/A000045

    Generator id:
        identity
    Desciption:
        f(x) = x

    Generator id:
        log_gen
    Desciption:
        Logarithmic generator.

    Generator id:
        mersenne
    Desciption:
        Generate 2^n - 1.
        https://oeis.org/A001348

    Generator id:
        triangular_numbers
    Desciption:
        Triangular numbers: a(n) = C(n+1,2) = n(n+1)/2 = 0+1+2+...+n.
        http://oeis.org/A000217


An other example:

.. code-block:: bash

    # Hide the message - LSB with a set defined by the identity function (f(x) = x).
    stegano-lsb-set hide -i ./tests/sample-files/Montenach.png --generator identity -m 'I like steganography.' -o ./enc-identity.png

    # Hide the message - LSB only.
    stegano-lsb hide -i ./tests/sample-files/Montenach.png -m 'I like steganography.' -o ./enc.png

    # Check if the two generated files are the same.
    sha1sum ./enc-identity.png ./enc.png

    # The output of lsb is given to lsb-set.
    stegano-lsb-set reveal -i ./enc.png --generator identity

    # The output of lsb-set is given to lsb.
    stegano-lsb reveal -i ./enc-identity.png


Hide and reveal a text message with the red portion of a pixel
--------------------------------------------------------------

.. code-block:: bash

    $ stegano-red hide --help
    usage: stegano-red hide [-h] [-i INPUT_IMAGE_FILE] [-m SECRET_MESSAGE]
                        [-o OUTPUT_IMAGE_FILE]

    optional arguments:
    -h, --help            show this help message and exit
    -i INPUT_IMAGE_FILE, --input INPUT_IMAGE_FILE
                        Image file
    -m SECRET_MESSAGE     Your secret message to hide (non binary).
    -o OUTPUT_IMAGE_FILE, --output OUTPUT_IMAGE_FILE
                        Image file

    $ stegano-red hide -i ./tests/sample-files/Lenna.png -m 'Basic steganography technique.' -o ~/Lenna1.png

    $ stegano-red reveal -i ~/Lenna1.png
    Basic steganography technique.
