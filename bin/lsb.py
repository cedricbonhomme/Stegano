#!/usr/bin/env python
# Stegano - Stegano is a pure Python steganography module.
# Copyright (C) 2010-2024 Cédric Bonhomme - https://www.cedricbonhomme.org
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

import inspect

import crayons

try:
    from stegano import lsb
    from stegano.lsb import generators
except Exception:
    print("Install stegano: pipx install Stegano")

import argparse

from stegano import tools


class ValidateGenerator(argparse.Action):
    def __call__(self, parser, args, values, option_string=None):
        valid_generators = [
            generator[0]
            for generator in inspect.getmembers(generators, inspect.isfunction)
        ]
        # Verify that the generator is valid
        generator = values[0]
        if generator not in valid_generators:
            raise ValueError("Unknown generator: %s" % generator)
        # Set the generator_function arg of the parser
        setattr(args, self.dest, values)


def main():
    parser = argparse.ArgumentParser(prog="stegano-lsb")
    subparsers = parser.add_subparsers(
        help="sub-command help", dest="command", required=True
    )

    # Subparser: Hide
    parser_hide = subparsers.add_parser("hide", help="hide help")
    # Original image
    parser_hide.add_argument(
        "-i",
        "--input",
        dest="input_image_file",
        required=True,
        help="Input image file.",
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

    # Generator
    parser_hide.add_argument(
        "-g",
        "--generator",
        dest="generator_function",
        action=ValidateGenerator,
        nargs="*",
        required=False,
        default=None,
        help="Generator (with optional arguments)",
    )

    # Shift the message to hide
    parser_hide.add_argument(
        "-s", "--shift", dest="shift", default=0, help="Shift for the generator"
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

    # Image containing the secret
    parser_hide.add_argument(
        "-o",
        "--output",
        dest="output_image_file",
        required=True,
        help="Output image containing the secret.",
    )

    # Subparser: Reveal
    parser_reveal = subparsers.add_parser("reveal", help="reveal help")
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
        help="Specify the encoding of the message to reveal."
        " UTF-8 (default) or UTF-32LE.",
    )

    # Generator
    parser_reveal.add_argument(
        "-g",
        "--generator",
        dest="generator_function",
        action=ValidateGenerator,
        nargs="*",
        required=False,
        help="Generator (with optional arguments)",
    )

    # Shift the message to reveal
    parser_reveal.add_argument(
        "-s", "--shift", dest="shift", default=0, help="Shift for the generator"
    )
    parser_reveal.add_argument(
        "-o",
        dest="secret_binary",
        help="Output for the binary secret (Text or any binary file).",
    )

    # Subparser: List generators
    subparsers.add_parser("list-generators", help="list-generators help")

    arguments = parser.parse_args()

    if arguments.command != "list-generators":
        if not arguments.generator_function:
            generator = None
        else:
            try:
                if arguments.generator_function[0] == "LFSR":
                    # Compute the size of the image for use by the LFSR generator if needed
                    tmp = tools.open_image(arguments.input_image_file)
                    size = tmp.width * tmp.height
                    tmp.close()
                    arguments.generator_function.append(size)
                if len(arguments.generator_function) > 1:
                    generator = getattr(generators, arguments.generator_function[0])(
                        *[int(e) for e in arguments.generator_function[1:]]
                    )
                else:
                    generator = getattr(generators, arguments.generator_function[0])()

            except AttributeError:
                print(f"Unknown generator: {arguments.generator_function}")
                exit(1)

    if arguments.command == "hide":
        if arguments.secret_message is not None:
            secret = arguments.secret_message
        elif arguments.secret_file != "":
            secret = tools.binary2base64(arguments.secret_file)

        img_encoded = lsb.hide(
            image=arguments.input_image_file,
            message=secret,
            generator=generator,
            shift=int(arguments.shift),
            encoding=arguments.encoding,
        )
        try:
            img_encoded.save(arguments.output_image_file)
        except Exception as e:
            # If hide() returns an error (Too long message).
            print(e)

    elif arguments.command == "reveal":
        try:
            secret = lsb.reveal(
                encoded_image=arguments.input_image_file,
                generator=generator,
                shift=int(arguments.shift),
                encoding=arguments.encoding,
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

    elif arguments.command == "list-generators":
        all_generators = inspect.getmembers(generators, inspect.isfunction)
        for generator in all_generators:
            print("Generator id:")
            print(f"    {crayons.green(generator[0], bold=True)}")
            print("Desciption:")
            print(f"    {generator[1].__doc__}")
