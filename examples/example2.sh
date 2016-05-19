#!/bin/sh

#
# Test the LSB method with sets.
#

echo  "We're going to test a little Stéganô..."

echo "Hide the message  with the Sieve of Eratosthenes..."
lsb-set --hide -i ./pictures/Montenach.png -o ./surprise.png --generator eratosthenes -m 'Joyeux Noël!'
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
