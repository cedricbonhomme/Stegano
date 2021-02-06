#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Stegano - Stegano is a pure Python steganography module.
# Copyright (C) 2010-2021 Cédric Bonhomme - https://www.cedricbonhomme.org
#
# For more information : https://github.com/cedricbonhomme/Stegano
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

__author__ = "Cedric Bonhomme"
__version__ = "$Revision: 0.8 $"
__date__ = "$Date: 2016/08/04 $"
__revision__ = "$Date: 2019/06/01 $"
__license__ = "GPLv3"

import argparse

try:
    from stegano import lsb
except:
    print("Install Stegano: pipx install Stegano")

from stegano import tools

def main():
    parser = argparse.ArgumentParser(prog='stegano-lsb')
    subparsers = parser.add_subparsers(help='sub-command help', dest='command')

    # Subparser: Hide
    parser_hide = subparsers.add_parser('hide', help='hide help')
    # Original image
    parser_hide.add_argument("-i", "--input", dest="input_image_file",
                    required=True, help="Input image file.")
    parser_hide.add_argument("-e", "--encoding", dest="encoding",
                    choices=tools.ENCODINGS.keys(), default='UTF-8',
                    help="Specify the encoding of the message to hide." +
                    " UTF-8 (default) or UTF-32LE.")

    group_secret = parser_hide.add_mutually_exclusive_group(required=True)
    # Non binary secret message to hide
    group_secret.add_argument("-m", dest="secret_message",
                    help="Your secret message to hide (non binary).")
    # Binary secret message to hide
    group_secret.add_argument("-f", dest="secret_file",
                    help="Your secret to hide (Text or any binary file).")

    # Image containing the secret
    parser_hide.add_argument("-o", "--output", dest="output_image_file",
                    required=True, help="Output image containing the secret.")

    # Shift the message to hide
    parser_hide.add_argument("-s", "--shift", dest="shift", default=0,
                    help="Shift for the message to hide")

    # Subparser: Reveal
    parser_reveal = subparsers.add_parser('reveal', help='reveal help')
    parser_reveal.add_argument("-i", "--input", dest="input_image_file",
                    required=True, help="Input image file.")
    parser_reveal.add_argument("-e", "--encoding", dest="encoding",
                    choices=tools.ENCODINGS.keys(), default='UTF-8',
                    help="Specify the encoding of the message to reveal." +
                    " UTF-8 (default) or UTF-32LE.")
    parser_reveal.add_argument("-o", dest="secret_binary",
                    help="Output for the binary secret (Text or any binary file).")
    # Shift the message to reveal
    parser_reveal.add_argument("-s", "--shift", dest="shift", default=0,
                    help="Shift for the reveal")

    arguments = parser.parse_args()


    if arguments.command == 'hide':
        if arguments.secret_message != None:
            secret = arguments.secret_message
        elif arguments.secret_file != None:
            secret = tools.binary2base64(arguments.secret_file)

        img_encoded = lsb.hide(arguments.input_image_file, secret,
                               arguments.encoding, int(arguments.shift))
        try:
            img_encoded.save(arguments.output_image_file)
        except Exception as e:
            # If hide() returns an error (Too long message).
            print(e)

    elif arguments.command == 'reveal':
        secret = lsb.reveal(arguments.input_image_file, arguments.encoding,
                            int(arguments.shift))
        if arguments.secret_binary != None:
            data = tools.base642binary(secret)
            with open(arguments.secret_binary, "wb") as f:
                f.write(data)
        else:
            print(secret)
