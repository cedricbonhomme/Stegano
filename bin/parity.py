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
__date__ = "$Date: 2016/08/25 $"
__license__ = "GPLv3"

import argparse

from PIL import Image

try:
    from stegano.steganalysis import parity
except Exception:
    print("Install Stegano: pipx install Stegano")


def main():
    parser = argparse.ArgumentParser(prog="stegano-steganalysis-parity")
    parser.add_argument(
        "-i",
        "--input",
        dest="input_image_file",
        required=True,
        help="Input image file.",
    )
    parser.add_argument(
        "-o",
        "--output",
        dest="output_image_file",
        required=True,
        help="Output image file.",
    )
    arguments = parser.parse_args()

    input_image_file = Image.open(arguments.input_image_file)
    output_image = parity.steganalyse(input_image_file)
    output_image.save(arguments.output_image_file)
