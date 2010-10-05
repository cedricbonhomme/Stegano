# -*- coding: utf-8 -*-

__author__ = "Cedric Bonhomme"
__version__ = "$Revision: 0.1 $"
__date__ = "$Date: 2010/10/01 $"

from PIL import Image

def hide(img, message):
    """
    Hide a message (string) in an image.

    Use the red portion of a pixel (r, g, b) tuple to
    hide the message string characters as ASCII values.
    The red value of the first pixel is used for length of string.
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
    Find a message in an image.

    Check the red portion of an pixel (r, g, b) tuple for
    hidden message characters (ASCII values).
    The red value of the first pixel is used for length of string.
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
    from optparse import OptionParser
    usage = "usage: %prog hide|reveal [options]"
    parser = OptionParser(usage)
    parser.add_option("-i", "--input", dest="input_image_file",
                    help="Image file")
    parser.add_option("-o", "--output", dest="output_image_file",
                    help="Image file")
    parser.add_option("-s", "--secret", dest="secret",
                    help="Your secret (Message, Image, Music or any binary file.)")
    parser.set_defaults(input_image_file = './pictures/Lenna.png',
                        output_image_file = './pictures/Lenna_enc.png',
                        secret = 'Hello World!')

    (options, args) = parser.parse_args()


    if sys.argv[1] == "hide":
        img = Image.open(options.input_image_file)
        img_encoded = hide(img, options.secret)
        img_encoded.save(options.output_image_file)

    elif sys.argv[1] == "reveal":
        img = Image.open(options.input_image_file)
        print reveal(img)