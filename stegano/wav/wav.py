#!/usr/bin/env python
# Stegano - Stéganô is a basic Python Steganography module.
# Copyright (C) 2010-2024  Cédric Bonhomme - https://www.cedricbonhomme.org
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
__version__ = "$Revision: 0.2 $"
__date__ = "$Date: 2010/10/01 $"
__revision__ = "$Date: 2017/02/06 $"
__license__ = "GPLv3"

from typing import IO, Union

import wave

def hide(input_file: Union[str, IO[bytes]], message: str, output_file: Union[str, IO[bytes]]):
    """
    Hide a message (string) in a .wav audio file.

    Use the lsb of each sample to hide the message string characters as ASCII values.
    The first eight bits are used for message_length of the string.
    """
    message_length = len(message)
    assert message_length != 0, "message message_length is zero"
    # TODO messages in audio files could likely be much longer in most cases
    assert message_length < 255, "message is too long"

    output = wave.open(output_file, "wb")
    with wave.open(input_file, "rb") as input:
        pass
        # TODO


def reveal(input_file: Union[str, IO[bytes]]):
    """
    Find a message in an image.

    Check the lsb of each sample for hidden message characters (ASCII values).
    The first eight bits are used for message_length of the string.
    """
    message = ""
    with wave.open(input_file, "rb") as input:
        pass
        # TODO
    return message
