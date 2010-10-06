#!/bin/sh

#hg clone http://bitbucket.org/cedricbonhomme/stegano/
#cd stegano
cd ..
wget http://www.gnu.org/music/free-software-song.ogg
./lsb-s.py --hide -i ./pictures/Montenach.png -o ./pictures/Montenach_enc.png -f ./free-software-song.ogg
rm free-software-song.ogg
./lsb-s.py --reveal -i ./pictures/Montenach_enc.png -b ./zik.ogg
