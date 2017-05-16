Using Stéganô as a Python module
================================

You can find more examples in the
`unit tests directory <https://github.com/cedricbonhomme/Stegano/tree/master/tests>`_.

LSB method
----------

.. code-block:: python

    Python 3.5.1 (default, Dec  7 2015, 11:33:57)
    [GCC 4.9.2] on linux
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

    Python 3.5.1 (default, Dec  7 2015, 11:33:57)
    [GCC 4.9.2] on linux
    Type "help", "copyright", "credits" or "license" for more information.
    >>> from stegano import lsbset
    >>> from stegano.lsbset import generators

    # Hide a secret with the Sieve of Eratosthenes
    >>> secret_message = "Hello World!"
    >>> secret_image = lsbset.hide("./tests/sample-files/Lenna.png",
                                    secret_message,
                                    generators.eratosthenes())
    >>> secret_image.save("./image.png")

    # Try to decode with another generator
    >>> message = lsbset.reveal("./image.png", generators.fibonacci())
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "/home/cedric/projects/Stegano/stegano/lsbset/lsbset.py", line 111, in reveal
        for color in img_list[generated_number]:
    IndexError: list index out of range

    # Decode with Eratosthenes
    >>> message = lsbset.reveal("./image.png", generators.eratosthenes())
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



Description field of the image
------------------------------

For JPEG and TIFF images.

.. code-block:: python

    Python 3.5.1 (default, Dec  7 2015, 11:33:57)
    [GCC 4.9.2] on linux
    Type "help", "copyright", "credits" or "license" for more information.
    >>> from stegano import exifHeader
    >>> secret = exifHeader.hide("./tests/sample-files/20160505T130442.jpg",
                            "./image.jpg", secret_message="Hello world!")
    >>> print(exifHeader.reveal("./image.jpg"))
