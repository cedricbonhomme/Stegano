#!/bin/sh

#
# Test the LSB method with sets.
#


echo "Hide the message  with Sieve of Eratosthenes..."
slsb-set --hide -i ./pictures/Ginnifer-Goodwin.png -o ./surprise.png --generator eratosthenes -m 'Probably the most beautiful woman in the world.'
echo ""

echo "Steganalysis of the original photo..."
steganalysis-parity -i ./pictures/Ginnifer-Goodwin.png -o ./surprise_st_original.png

echo "Steganalysis of the secret photo..."
steganalysis-parity -i ./surprise.png -o ./surprise_st_secret.png
echo ""

echo "Reveal with Sieve of Eratosthenes..."
echo "The secret is:"
slsb-set --reveal --generator eratosthenes -i ./surprise.png