#!/usr/bin/env python
# Stegano - Stegano is a pure Python steganography module.
# Copyright (C) 2010-2025 Cédric Bonhomme - https://www.cedricbonhomme.org
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
__version__ = "$Revision: 0.7 $"
__date__ = "$Date: 2016/03/18 $"
__revision__ = "$Date: 2019/06/04 $"
__license__ = "GPLv3"

try:
    from stegano import wav
except Exception:
    print("Install stegano: pipx install Stegano")

import argparse

from stegano import tools


def main():
    parser = argparse.ArgumentParser(prog="stegano-lsb")
    subparsers = parser.add_subparsers(
        help="sub-command help", dest="command", required=True
    )

    # Subparser: Hide
    parser_hide = subparsers.add_parser("hide", help="hide help")
    # Original audio
    parser_hide.add_argument(
        "-i",
        "--input",
        dest="input_audio_file",
        required=True,
        help="Input audio file.",
    )
    parser_hide.add_argument(
        "-e",
        "--encoding",
        dest="encoding",
        choices=tools.ENCODINGS.keys(),
        default="UTF-8",
        help="Specify the encoding of the message to hide."
        " UTF-8 (default) or UTF-32LE.",
    )

    group_secret = parser_hide.add_mutually_exclusive_group(required=True)
    # Non binary secret message to hide
    group_secret.add_argument(
        "-m", dest="secret_message", help="Your secret message to hide (non binary)."
    )
    # Binary secret message to hide
    group_secret.add_argument(
        "-f", dest="secret_file", help="Your secret to hide (Text or any binary file)."
    )

    # Audio containing the secret
    parser_hide.add_argument(
        "-o",
        "--output",
        dest="output_audio_file",
        required=True,
        help="Output audio containing the secret.",
    )

    # Subparser: Reveal
    parser_reveal = subparsers.add_parser("reveal", help="reveal help")
    parser_reveal.add_argument(
        "-i",
        "--input",
        dest="input_audio_file",
        required=True,
        help="Input audio file.",
    )
    parser_reveal.add_argument(
        "-e",
        "--encoding",
        dest="encoding",
        choices=tools.ENCODINGS.keys(),
        default="UTF-8",
        help="Specify the encoding of the message to reveal."
        " UTF-8 (default) or UTF-32LE.",
    )

    arguments = parser.parse_args()

    if arguments.command == "hide":
        if arguments.secret_message is not None:
            secret = arguments.secret_message
        elif arguments.secret_file != "":
            secret = tools.binary2base64(arguments.secret_file)

        wav.hide(
            input_file=arguments.input_audio_file,
            message=secret,
            encoding=arguments.encoding,
            output_file=arguments.output_audio_file,
        )

    elif arguments.command == "reveal":
        try:
            secret = wav.reveal(
                input_file=arguments.input_audio_file, encoding=arguments.encoding
            )
        except IndexError:
            print("Impossible to detect message.")
            exit(0)
        if arguments.secret_binary is not None:
            data = tools.base642binary(secret)
            with open(arguments.secret_binary, "wb") as f:
                f.write(data)
        else:
            print(secret)
