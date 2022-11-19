Using Stegano as a Python module
================================

You can find more examples in the
`unit tests directory <https://git.sr.ht/~cedric/stegano/tree/master/tests>`_.

LSB method
----------

.. code-block:: python

    Python 3.11.0 (main, Oct 31 2022, 15:15:22) [GCC 12.2.0] on linux
    Type "help", "copyright", "credits" or "license" for more information.
    >>> from stegano import lsb
    >>> secret = lsb.hide("./tests/sample-files/Lenna.png", "Hello world!")
    >>> secret.save("./Lenna-secret.png")
    >>> print(lsb.reveal("./Lenna-secret.png"))
    Hello world!



LSB method with sets
--------------------

Sets are used in order to select the pixels where the message will be hidden.

.. code-block:: python

    Python 3.11.0 (main, Oct 31 2022, 15:15:22) [GCC 12.2.0] on linux
    Type "help", "copyright", "credits" or "license" for more information.
    >>> from stegano import lsb
    >>> from stegano.lsb import generators

    # Hide a secret with the Sieve of Eratosthenes
    >>> secret_message = "Hello World!"
    >>> secret_image = lsb.hide("./tests/sample-files/Lenna.png", secret_message, generators.eratosthenes())
    >>> secret_image.save("./image.png")

    # Try to decode with another generator
    >>> message = lsb.reveal("./image.png", generators.fibonacci())
    Traceback (most recent call last):
    File "/Users/flavien/.local/share/virtualenvs/Stegano-sY_cwr69/bin/stegano-lsb", line 6, in <module>
        sys.exit(main())
    File "/Users/flavien/Perso/dev/Stegano/bin/lsb.py", line 190, in main
        img_encoded = lsb.hide(
    File "/Users/flavien/Perso/dev/Stegano/stegano/lsb/lsb.py", line 63, in hide
        hider.encode_pixel((col, row))
    File "/Users/flavien/Perso/dev/Stegano/stegano/tools.py", line 165, in encode_pixel
        r, g, b, *a = self.encoded_image.getpixel(coordinate)
    File "/Users/flavien/.local/share/virtualenvs/Stegano-sY_cwr69/lib/python3.10/site-packages/PIL/Image.py", line 1481, in getpixel
        return self.im.getpixel(xy)
    IndexError: image index out of range

    # Decode with Eratosthenes
    >>> message = lsb.reveal("./image.png", generators.eratosthenes())
    >>> message
    'Hello World!'

    >>> # Generators available
    >>> import inspect
    >>> all_generators = inspect.getmembers(generators, inspect.isfunction)
    >>> for generator in all_generators:
    ...     print(generator[0], generator[1].__doc__)
    ...
    Dead_Man_Walking None
    OEIS_A000217
        http://oeis.org/A000217
        Triangular numbers: a(n) = C(n+1,2) = n(n+1)/2 = 0+1+2+...+n.

    ackermann
        Ackermann number.

    carmichael None
    eratosthenes
        Generate the prime numbers with the sieve of Eratosthenes.

    eratosthenes_composite
        Generate the composite numbers with the sieve of Eratosthenes.

    fermat
        Generate the n-th Fermat Number.

    fibonacci
        A generator for Fibonacci numbers, goes to next number in series on each call.
        This generator start at 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597, 2584, 4181, 6765, 10946, ...
        See: http://oeis.org/A000045

    identity
        f(x) = x

    log_gen
        Logarithmic generator.

    mersenne
        Generate 2^n-1.

    syracuse
        Generate the sequence of Syracuse.

    shi_tomashi Shi-Tomachi corner generator of the given points
        https://docs.opencv.org/4.x/d4/d8c/tutorial_py_shi_tomasi.html

    triangular_numbers Triangular numbers: a(n) = C(n+1,2) = n(n+1)/2 = 0+1+2+...+n.
        http://oeis.org/A000217



Description field of the image
------------------------------

For JPEG and TIFF images.

.. code-block:: python

    Python 3.11.0 (main, Oct 31 2022, 15:15:22) [GCC 12.2.0] on linux
    Type "help", "copyright", "credits" or "license" for more information.
    >>> from stegano import exifHeader
    >>> secret = exifHeader.hide("./tests/sample-files/20160505T130442.jpg",
                            "./image.jpg", secret_message="Hello world!")
    >>> print(exifHeader.reveal("./image.jpg"))
