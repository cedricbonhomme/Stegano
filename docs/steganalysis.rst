Steganalysis
============

Parity
------

.. code-block:: bash

    # Hide the message  with Sieve of Eratosthenes
    lsb-set hide -i ./tests/sample-files/Ginnifer-Goodwin.png -o ./surprise.png --generator eratosthenes -m 'Very important message.'

    # Steganalysis of the original photo
    steganalysis-parity -i ./tests/sample-files/Ginnifer-Goodwin.png -o ./surprise_st_original.png

    # Steganalysis of the secret photo
    steganalysis-parity -i ./surprise.png -o ./surprise_st_secret.png

    # Reveal with Sieve of Eratosthenes
    lsb-set reveal --generator eratosthenes -i ./surprise.png
