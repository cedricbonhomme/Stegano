Using Stegano in command line
=============================

The command ``stegano-lsb``
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Hide and reveal a message with the LSB method.

Display help
------------

.. code-block:: bash

    $ stegano-lsb --help
    usage: stegano-lsb [-h] {hide,reveal,list-generators} ...

    positional arguments:
    {hide,reveal,list-generators}
                            sub-command help
        hide                hide help
        reveal              reveal help
        list-generators     list-generators help

    options:
    -h, --help            show this help message and exit


.. code-block:: bash

    $ stegano-lsb hide --help
    usage: stegano-lsb hide [-h] -i INPUT_IMAGE_FILE [-e {UTF-8,UTF-32LE}] [-g [GENERATOR_FUNCTION ...]] [-s SHIFT] (-m SECRET_MESSAGE | -f SECRET_FILE) -o OUTPUT_IMAGE_FILE

    options:
    -h, --help            show this help message and exit
    -i INPUT_IMAGE_FILE, --input INPUT_IMAGE_FILE
                            Input image file.
    -e {UTF-8,UTF-32LE}, --encoding {UTF-8,UTF-32LE}
                            Specify the encoding of the message to hide. UTF-8 (default) or UTF-32LE.
    -g [GENERATOR_FUNCTION ...], --generator [GENERATOR_FUNCTION ...]
                            Generator (with optional arguments)
    -s SHIFT, --shift SHIFT
                            Shift for the generator
    -m SECRET_MESSAGE     Your secret message to hide (non binary).
    -f SECRET_FILE        Your secret to hide (Text or any binary file).
    -o OUTPUT_IMAGE_FILE, --output OUTPUT_IMAGE_FILE
                            Output image containing the secret.


.. code-block:: bash

    $ stegano-lsb reveal --help
    usage: stegano-lsb reveal [-h] -i INPUT_IMAGE_FILE [-e {UTF-8,UTF-32LE}] [-g [GENERATOR_FUNCTION ...]] [-s SHIFT] [-o SECRET_BINARY]

    options:
    -h, --help            show this help message and exit
    -i INPUT_IMAGE_FILE, --input INPUT_IMAGE_FILE
                            Input image file.
    -e {UTF-8,UTF-32LE}, --encoding {UTF-8,UTF-32LE}
                            Specify the encoding of the message to reveal. UTF-8 (default) or UTF-32LE.
    -g [GENERATOR_FUNCTION ...], --generator [GENERATOR_FUNCTION ...]
                            Generator (with optional arguments)
    -s SHIFT, --shift SHIFT
                            Shift for the generator
    -o SECRET_BINARY      Output for the binary secret (Text or any binary file).


Hide and reveal a text message
------------------------------

.. code-block:: bash

    $ stegano-lsb hide -i ./tests/sample-files/Lenna.png -m 'Hello World!' -o ./Lenna_enc.png
    $ stegano-lsb reveal -i ./Lenna_enc.png
    Hello World!

Specify an encoding
-------------------

.. code-block:: bash

    $ stegano-lsb hide -i ./tests/sample-files/Lenna.png -m 'I love 🍕 and 🍫.' -e UTF-32LE -o ./Lenna_enc.png
    $ stegano-lsb reveal -i ./Lenna_enc.png
    I love 🍕 and 🍫.

The default encoding is UTF-8.

Hide and reveal a binary file
-----------------------------

.. code-block:: bash

    $ wget http://www.gnu.org/music/free-software-song.ogg
    $ stegano-lsb hide -i ./tests/sample-files/Montenach.png -f ./free-software-song.ogg -o ./Montenach_enc.png
    $ rm free-software-song.ogg
    $ stegano-lsb reveal -i ./Montenach_enc.png -o ./song.ogg



Sets are used in order to select the pixels where the message will be hidden.

Hide and reveal a text message with set
---------------------------------------

.. code-block:: bash

    # Hide the message with the Sieve of Eratosthenes
    $ stegano-lsb hide -i ./tests/sample-files/Montenach.png --generator eratosthenes -m 'Joyeux Noël!' -o ./surprise.png

    # Try to reveal with Mersenne numbers
    $ stegano-lsb reveal --generator mersenne -i ./surprise.png

    # Try to reveal with fermat numbers
    $ stegano-lsb reveal --generator fermat -i ./surprise.png

    # Try to reveal with carmichael numbers
    $ stegano-lsb reveal --generator carmichael -i ./surprise.png

    # Try to reveal with Sieve of Eratosthenes
    $ stegano-lsb reveal --generator eratosthenes -i ./surprise.png


Sometimes it can be useful to skip the first values of a set. For example if you want
to hide several messages or because due to the selected generator
(Fibonacci starts with 0, 1, 1, etc.). Or maybe you just want to add more complexity.
In this case, simply use the optional arguments ``--shift`` or ``-s``:


.. code-block:: bash

    $ stegano-lsb hide -i ./tests/sample-files/Lenna.png -m 'Shifted secret message' -o ~/Lenna1.png --shift 7
    $ stegano-lsb reveal -i ~/Lenna1.png --shift 7
    Shifted secret message


List all available generators
------------------------------

.. code-block:: bash

    $ stegano-lsb list-generators
    Generator id:
        ackermann
    Desciption:
        Ackermann number.

    Generator id:
        ackermann_naive
    Desciption:
        Ackermann number.

    Generator id:
        carmichael
    Desciption:
        Composite numbers n such that a^(n-1) == 1 (mod n) for every a coprime
        to n.
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
        Generate 2^p - 1, where p is prime.
        https://oeis.org/A001348

    Generator id:
        triangular_numbers
    Desciption:
        Triangular numbers: a(n) = C(n+1,2) = n(n+1)/2 = 0+1+2+...+n.
        http://oeis.org/A000217







The command ``stegano-red``
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Hide and reveal a text message with the red portion of a pixel.

Display help
------------

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

Hide and reveal a text message
------------------------------

.. code-block:: bash

    $ stegano-red hide -i ./tests/sample-files/Lenna.png -m 'Basic steganography technique.' -o ~/Lenna1.png
    $ stegano-red reveal -i ~/Lenna1.png
    Basic steganography technique.
