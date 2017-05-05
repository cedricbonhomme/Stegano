Steganalysis
============

Parity
------

.. code-block:: bash

    # Hide the message  with Sieve of Eratosthenes
    stegano-lsb-set hide -i ./tests/sample-files/20160505T130442.jpg -o ./surprise.png --generator eratosthenes -m 'Very important message.'

    # Steganalysis of the original photo
    stegano-steganalysis-parity -i ./tests/sample-files/20160505T130442.jpg -o ./surprise_st_original.png

    # Steganalysis of the secret photo
    stegano-steganalysis-parity -i ./surprise.png -o ./surprise_st_secret.png

    # Reveal with Sieve of Eratosthenes
    stegano-lsb-set reveal -i ./surprise.png --generator eratosthenes
