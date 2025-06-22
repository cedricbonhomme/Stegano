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

import wave
from typing import IO, Union

from stegano import tools


def hide(
    input_file: Union[str, IO[bytes]],
    message: str,
    output_file: Union[str, IO[bytes]],
    encoding: str = "UTF-8",
):
    """
    Hide a message (string) in a .wav audio file.

    Use the lsb of each PCM encoded sample to hide the message string characters as ASCII values.
    The first eight bits are used for message_length of the string.
    """
    message_length = len(message)
    assert message_length != 0, "message message_length is zero"
    assert message_length < 255, "message is too long"

    output = wave.open(output_file, "wb")
    with wave.open(input_file, "rb") as input:
        # get .wav params
        nchannels, sampwidth, framerate, nframes, comptype, _ = input.getparams()
        assert comptype == "NONE", "only uncompressed files are supported"

        nsamples = nframes * nchannels

        message_bits = f"{message_length:08b}" + "".join(
            tools.a2bits_list(message, encoding)
        )
        assert len(message_bits) <= nsamples, "message is too long"

        # copy over .wav params to output
        output.setnchannels(nchannels)
        output.setsampwidth(sampwidth)
        output.setframerate(framerate)

        # encode message in frames
        frames = bytearray(input.readframes(nsamples))
        for i in range(nsamples):
            if i < len(message_bits):
                if message_bits[i] == "0":
                    frames[i] = frames[i] & ~1
                else:
                    frames[i] = frames[i] | 1

        # write out
        output.writeframes(frames)


def reveal(input_file: Union[str, IO[bytes]], encoding: str = "UTF-8"):
    """
    Find a message in an image.

    Check the lsb of each PCM encoded sample for hidden message characters (ASCII values).
    The first eight bits are used for message_length of the string.
    """
    message = ""
    encoding_len = tools.ENCODINGS[encoding]
    with wave.open(input_file, "rb") as input:
        nchannels, _, _, nframes, comptype, _ = input.getparams()
        assert comptype == "NONE", "only uncompressed files are supported"

        nsamples = nframes * nchannels
        frames = bytearray(input.readframes(nsamples))

        # Read first 8 bits for message length
        length_bits = ""
        for i in range(8):
            length_bits += str(frames[i] & 1)
        message_length = int(length_bits, 2)

        # Read message bits
        message_bits = ""
        for i in range(8, 8 + message_length * encoding_len):
            message_bits += str(frames[i] & 1)

        # Convert bits to string
        chars = [
            chr(int(message_bits[i : i + encoding_len], 2))
            for i in range(0, len(message_bits), encoding_len)
        ]
        message = "".join(chars)
    return message
