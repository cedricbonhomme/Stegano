#! /usr/local/bin/python
#-*- coding: utf-8 -*-

__author__ = "Cedric Bonhomme"
__version__ = "$Revision: 0.1 $"
__date__ = "$Date: 2010/10/01 $"

import tools

from PIL import Image

def encode_image(img, message):
    """
    Hide a message (string) in an image with the
    LSB (Less Significant Bit) technic.
    """
    encoded = img.copy()
    width, height = img.size
    index = 0
    
    message = message + '~~~'
    message_bits = tools.a2bits(message)
    
    for row in range(height):
        for col in range(width):

            if index + 3 <= len(message_bits) :

                (r, g, b) = img.getpixel((col, row))
                    
                # Convert in to bits
                r_bits = tools.bs(r)
                g_bits = tools.bs(g)
                b_bits = tools.bs(b)

                # Replace (in a list) the least significant bit
                # by the bit of the message to hide
                list_r_bits = list(r_bits)
                list_g_bits = list(g_bits)
                list_b_bits = list(b_bits)
                list_r_bits[-1] = message_bits[index]
                list_g_bits[-1] = message_bits[index + 1]
                list_b_bits[-1] = message_bits[index + 2]

                # Convert lists to a strings
                r_bits = "".join(list_r_bits)
                g_bits = "".join(list_g_bits)
                b_bits = "".join(list_b_bits)
                
                # Convert strings of bits to int
                r = int(r_bits, 2)
                g = int(g_bits, 2)
                b = int(b_bits, 2)

                # Save the new pixel
                encoded.putpixel((col, row), (r, g , b))

            index += 3

    return encoded

def decode_image(img):
    """
    Find a message in an encoded image (with the
    LSB technic).
    """
    width, height = img.size
    bits = ""
    index = 0
    for row in range(height):
        for col in range(width):
            r, g, b = img.getpixel((col, row))

            bits += tools.bs(r)[-1] + tools.bs(g)[-1] + tools.bs(b)[-1]

            if len(bits) >= 8:
                if chr(int(bits[-8:], 2)) == '~':
                    list_of_string_bits = ["".join(list(bits[i*8:(i*8)+8])) for i in range(0, len(bits)/8)]

                    list_of_character = [chr(int(elem, 2)) for elem in list_of_string_bits]
                    return "".join(list_of_character)[:-1]
    return ""


if __name__ == '__main__':
    # Point of entry in execution mode
    original_image_file = "./pictures/Lenna.png"
    encoded_image_file = "Lenna_enc.png"

    img = Image.open(original_image_file)

    secret_msg = "Avec la technique LSB (Least Significant Bit) l'oeil humain (un normal ;-))  ne voit plus la difference!"
    img_encoded = encode_image(img, secret_msg)


    if img_encoded:
        # Save it
        img_encoded.save(encoded_image_file)
        # Test it
        img2 = Image.open(encoded_image_file)
        print(decode_image(img2))