#!/usr/bin/env python
# Stegano - Stéganô is a basic Python Steganography module.
# Copyright (C) 2010-2026  Cédric Bonhomme - https://www.cedricbonhomme.org
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

    Use the LSB of each PCM encoded sample to hide the message bytes.
    The first eight bits are used for the length of the message in bytes.
    """
    if encoding not in tools.ENCODINGS:
        raise ValueError(f"Unsupported encoding: {encoding}")

    assert len(message) != 0, "message message_length is zero"
    message_bytes = message.encode(encoding)
    assert len(message_bytes) < 256, "message is too long"

    output = wave.open(output_file, "wb")
    with wave.open(input_file, "rb") as input:
        # get .wav params
        nchannels, sampwidth, framerate, nframes, comptype, _ = input.getparams()
        assert comptype == "NONE", "only uncompressed files are supported"

        nsamples = nframes * nchannels

        # The payload is the byte-length prefix (8 bits) followed by the
        # message encoded to bytes, 8 bits per byte.
        message_bits = "".join(
            bin(byte)[2:].rjust(8, "0")
            for byte in bytes([len(message_bytes)]) + message_bytes
        )
        assert len(message_bits) <= nsamples, "message is too long"

        # copy over .wav params to output
        output.setnchannels(nchannels)
        output.setsampwidth(sampwidth)
        output.setframerate(framerate)

        # Encode one bit per sample. PCM samples wider than one byte are
        # little-endian: the LSB of sample i is bit 0 of frames[i * sampwidth].
        frames = bytearray(input.readframes(nframes))
        for i, bit in enumerate(message_bits):
            if bit == "0":
                frames[i * sampwidth] = frames[i * sampwidth] & ~1
            else:
                frames[i * sampwidth] = frames[i * sampwidth] | 1

        # write out
        output.writeframes(frames)


def reveal(input_file: Union[str, IO[bytes]], encoding: str = "UTF-8"):
    """
    Find a message in a .wav audio file.

    Check the LSB of each PCM encoded sample for the hidden message bytes.
    The first eight bits are used for the length of the message in bytes.
    """
    if encoding not in tools.ENCODINGS:
        raise ValueError(f"Unsupported encoding: {encoding}")

    with wave.open(input_file, "rb") as input:
        _, sampwidth, _, nframes, comptype, _ = input.getparams()
        assert comptype == "NONE", "only uncompressed files are supported"

        frames = bytearray(input.readframes(nframes))

        # Read first 8 bits for the message length in bytes
        length_bits = ""
        for i in range(8):
            length_bits += str(frames[i * sampwidth] & 1)
        message_length = int(length_bits, 2)

        # Read the message bytes
        message_bytes = bytearray()
        for i in range(message_length):
            byte_bits = ""
            for j in range(8):
                byte_bits += str(frames[(8 + i * 8 + j) * sampwidth] & 1)
            message_bytes.append(int(byte_bits, 2))

    try:
        return bytes(message_bytes).decode(encoding)
    except UnicodeDecodeError as exc:
        raise IndexError("Impossible to detect message.") from exc
