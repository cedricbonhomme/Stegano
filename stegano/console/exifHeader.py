#!/usr/bin/env python
# Stegano - Stegano is a pure Python steganography module.
# Copyright (C) 2010-2026 Cédric Bonhomme - https://www.cedricbonhomme.org
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
__version__ = "$Revision: 0.1 $"
__date__ = "$Date: 2017/02/06 $"
__license__ = "GPLv3"

import argparse

try:
    from stegano import exifHeader
except Exception:
    print("Install stegano: sudo pip install Stegano")


def main():
    parser = argparse.ArgumentParser(prog="stegano-exif")
    subparsers = parser.add_subparsers(help="sub-command help", dest="command")

    parser_hide = subparsers.add_parser("hide", help="hide help")
    parser_hide.add_argument(
        "-i", "--input", dest="input_image_file", help="Input image file."
    )
    parser_hide.add_argument(
        "-m", dest="secret_message", help="Your raw secret message to hide."
    )
    parser_hide.add_argument(
        "-o", "--output", dest="output_image_file", help="Output image file."
    )
    parser_hide.add_argument(
        "-f", "--secret-file", dest="secret_file", help="Your secret file to hide."
    )

    parser_reveal = subparsers.add_parser("reveal", help="reveal help")
    parser_reveal.add_argument(
        "-i", "--input", dest="input_image_file", help="Input image file."
    )

    arguments = parser.parse_args()

    if arguments.command == "hide" and arguments.secret_message:
        secret = exifHeader.hide(arguments.input_image_file, arguments.secret_message)
        secret.save(arguments.output_image_file)

    elif arguments.command == "hide" and arguments.secret_file:
        secret = exifHeader.hide(arguments.input_image_file, arguments.secret_file)
        secret.save(arguments.output_image_file)

    elif arguments.command == "reveal":
        secret = exifHeader.reveal(arguments.input_image_file)
        print(secret)
