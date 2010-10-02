# -*- coding: utf-8 -*-

__author__ = "Cedric Bonhomme"
__version__ = "$Revision: 0.1 $"
__date__ = "$Date: 2010/10/01 $"

from PIL import Image

def hide(img, message):
    """
    use the red portion of an image (r, g, b) tuple to
    hide the message string characters as ASCII values
    the red value of the first pixel is used for length of string  
    """
    length = len(message)
    # limit length of message to 255
    if length > 255:
        return False
    # use a copy of image to hide the text in
    encoded = img.copy()
    width, height = img.size
    index = 0
    for row in range(height):
        for col in range(width):
            (r, g, b) = img.getpixel((col, row))
            # first value is length of message
            if row == 0 and col == 0 and index < length:
                asc = length
            elif index <= length:
                c = message[index -1]
                asc = ord(c)
            else:
                asc = r
            encoded.putpixel((col, row), (asc, g , b))
            index += 1
    return encoded

def reveal(img):
    """
    check the red portion of an image (r, g, b) tuple for
    hidden message characters (ASCII values)
    the red value of the first pixel is used for length of string   
    """
    width, height = img.size
    message = ""
    index = 0
    for row in range(height):
        for col in range(width):
            r, g, b = img.getpixel((col, row))
            # first pixel r value is length of message
            if row == 0 and col == 0:
                length = r
            elif index <= length:
                message += chr(r)
            index += 1
    return message

if __name__ == '__main__':
    # Point of entry in execution mode
    original_image_file = "./pictures/Lenna.png"
    encoded_image_file = "./pictures/Lenna_enc.png"
    # at this point don't exceed 255 characters
    secret_message = "Parce que je le vaut bien!"
    
    img1 = Image.open(original_image_file)
    img_encoded = hide(img1, secret_message)

    if img_encoded:
        # Save it
        img_encoded.save(encoded_image_file)
        # Test it
        img2 = Image.open(encoded_image_file)
        print reveal(img2)
    else:
        print("text too long! (don't exeed 255 characters)") 