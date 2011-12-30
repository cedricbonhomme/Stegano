#!/bin/sh

# Some tests of the LSB method which uses sets (slsb-set). Sets are used in order to select the pixels where the
# message will be hidden.


# Hide the message - LSB with a set defined by the identity function (f(x) = x).
slsb-set --hide -i examples/pictures/Montenach.png -o ~/enc-identity.png --generator identity -m 'I like steganography.'

# Hide the message - LSB only.
slsb --hide -i examples/pictures/Montenach.png -o ~/enc.png -m 'I like steganography.'


# Check if the two generated files are the same.
sha1sum ~/enc-identity.png ~/enc.png 


# The output of slsb is given to slsb-set.
slsb-set --reveal -i ~/enc.png --generator identity 

# The output of slsb-set is given to slsb.
slsb --reveal -i ~/enc-identity.png
