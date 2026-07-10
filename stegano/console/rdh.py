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

__author__ = "Eesh Saxena"
__license__ = "GPLv3"

import argparse

from stegano import rdh, tools


def main():
    parser = argparse.ArgumentParser(prog="stegano-rdh")
    subparsers = parser.add_subparsers(
        help="sub-command help", dest="command", required=True
    )

    # Subparser: Hide
    parser_hide = subparsers.add_parser(
        "hide", help="Hide a message with histogram shifting."
    )
    parser_hide.add_argument(
        "-i",
        "--input",
        dest="input_image_file",
        required=True,
        help="Input (cover) image file.",
    )
    parser_hide.add_argument(
        "-e",
        "--encoding",
        dest="encoding",
        choices=tools.ENCODINGS.keys(),
        default="UTF-8",
        help="Encoding of the message to hide. UTF-8 (default) or UTF-32LE.",
    )
    parser_hide.add_argument(
        "-m",
        dest="secret_message",
        required=True,
        help="Your secret message to hide.",
    )
    parser_hide.add_argument(
        "-o",
        "--output",
        dest="output_image_file",
        required=True,
        help="Output image containing the secret.",
    )

    # Subparser: Reveal
    parser_reveal = subparsers.add_parser("reveal", help="Reveal a hidden message.")
    parser_reveal.add_argument(
        "-i",
        "--input",
        dest="input_image_file",
        required=True,
        help="Input image file.",
    )
    parser_reveal.add_argument(
        "-e",
        "--encoding",
        dest="encoding",
        choices=tools.ENCODINGS.keys(),
        default="UTF-8",
        help="Encoding of the message to reveal. UTF-8 (default) or UTF-32LE.",
    )

    # Subparser: Recover
    parser_recover = subparsers.add_parser(
        "recover", help="Losslessly recover the original cover image."
    )
    parser_recover.add_argument(
        "-i",
        "--input",
        dest="input_image_file",
        required=True,
        help="Input stego image file.",
    )
    parser_recover.add_argument(
        "-o",
        "--output",
        dest="output_image_file",
        required=True,
        help="Output file for the recovered cover image.",
    )

    arguments = parser.parse_args()

    if arguments.command == "hide":
        stego = rdh.hide(
            arguments.input_image_file,
            arguments.secret_message,
            arguments.encoding,
        )
        stego.save(arguments.output_image_file)
    elif arguments.command == "reveal":
        print(rdh.reveal(arguments.input_image_file, arguments.encoding))
    elif arguments.command == "recover":
        recovered = rdh.recover(arguments.input_image_file)
        recovered.save(arguments.output_image_file)


if __name__ == "__main__":
    main()
