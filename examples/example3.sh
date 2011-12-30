


slsb-set --hide -i examples/pictures/Montenach.png -o ~/enc-identity.png --generator identity -m 'I like steganography.'

slsb --hide -i examples/pictures/Montenach.png -o ~/enc.png -m 'I like steganography.'



sha1sum ~/enc-identity.png ~/enc.png 

slsb-set --reveal -i ~/enc.png --generator identity 

slsb --reveal -i ~/enc-identity.png
