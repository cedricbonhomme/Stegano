# -*- coding: utf-8 -*-

from PIL import Image

def encode_image(img, msg):
    """
    use the red portion of an image (r, g, b) tuple to
    hide the msg string characters as ASCII values
    the red value of the first pixel is used for length of string  
    """
    length = len(msg)
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
            # first value is length of msg
            if row == 0 and col == 0 and index < length:
                asc = length
            elif index <= length:
                c = msg[index -1]
                asc = ord(c)
            else:
                asc = r
            encoded.putpixel((col, row), (asc, g , b))
            index += 1
    return encoded


def decode_image(img):
    """
    check the red portion of an image (r, g, b) tuple for
    hidden message characters (ASCII values)
    the red value of the first pixel is used for length of string   
    """
    width, height = img.size
    msg = ""
    index = 0
    for row in range(height):
        for col in range(width):
            r, g, b = img.getpixel((col, row))
            # first pixel r value is length of message
            if row == 0 and col == 0:
                length = r
            elif index <= length:
                msg += chr(r)
            index += 1
    return msg


original_image_file = "./pictures/Lenna.png"
encoded_image_file = "./pictures/Lenna_enc.png"
img = Image.open(original_image_file)


# at this point don't exceed 255 characters
secret_msg = "Parce que je le vaut bien!"
img_encoded = encode_image(img, secret_msg)

if img_encoded:
    # save it ...
    img_encoded.save(encoded_image_file)
    # test it ...
    img2 = Image.open(encoded_image_file)
    print(decode_image(img2))
else:
    print("text too long! (don't exeed 255 characters)") 
