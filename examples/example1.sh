#!/bin/sh

wget http://www.gnu.org/music/free-software-song.ogg
slsb --hide -i ./pictures/Montenach.png -o ./pictures/Montenach_enc.png -f ./free-software-song.ogg
rm free-software-song.ogg
slsb --reveal -i ./pictures/Montenach_enc.png -b ./zik.ogg
