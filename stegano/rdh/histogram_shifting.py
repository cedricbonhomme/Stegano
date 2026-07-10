#!/usr/bin/env python
# Stegano - Stegano is a pure Python steganography module.
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

"""Reversible data hiding using histogram shifting.

Unlike the LSB technique, this is a *reversible* (a.k.a. lossless) data
hiding scheme: after the secret message is extracted, the original cover
image can be reconstructed pixel-for-pixel. This is useful when the cover
must not be permanently altered, for example medical, military or legal
imagery.

The scheme is the histogram-shifting method of

    Z. Ni, Y.-Q. Shi, N. Ansari and W. Su, "Reversible data hiding,"
    IEEE Transactions on Circuits and Systems for Video Technology,
    vol. 16, no. 3, pp. 354-362, 2006. doi:10.1109/TCSVT.2006.869964

Given the histogram of the (single 8-bit channel) sample values, a *peak*
point ``p`` (the most frequent value) and a *zero* point ``z`` (a value that
does not occur) are selected. All samples strictly between ``p`` and ``z``
are shifted by one towards ``z``, which frees the bin next to the peak. The
message is then embedded at the peak: a sample equal to ``p`` is left
untouched to encode a ``0`` and moved to the freed bin to encode a ``1``.
Extraction reverses both steps, so the cover image is fully restored.

Because ``p`` and ``z`` (and the payload length) are needed to extract and
to invert the shift, they are written into a small self-describing header
that occupies the least-significant bits of the first samples. The original
bits of those samples are themselves carried in the reversible payload, so
the header costs nothing in terms of reversibility.
"""

from typing import IO, List, Tuple, Union

from PIL import Image

from stegano import tools

__author__ = "Eesh Saxena"
__license__ = "GPLv3"

# 16-bit magic ("RD") + peak (8) + zero (8) + payload length (32).
_MAGIC = 0x5244
_HEADER_BITS = 16 + 8 + 8 + 32


def _flatten(image: Image.Image) -> List[int]:
    """Return the image samples as a flat list of ints.

    Every 8-bit sample (channel-interleaved for multi-band images) becomes an
    independent element of the returned list, so histogram shifting can treat
    an ``L``, ``RGB`` or ``RGBA`` image uniformly.
    """
    samples = list(image.tobytes())
    if not samples:
        raise ValueError("Cannot hide data in an empty image.")
    return samples


def _unflatten(samples: List[int], image: Image.Image) -> Image.Image:
    """Rebuild an image of the same mode/size from a flat list of samples."""
    return Image.frombytes(image.mode, image.size, bytes(samples))


def _int_to_bits(value: int, length: int) -> List[int]:
    return [(value >> (length - 1 - i)) & 1 for i in range(length)]


def _bits_to_int(bits: List[int]) -> int:
    value = 0
    for bit in bits:
        value = (value << 1) | bit
    return value


def _select_peak_zero(samples: List[int]) -> Tuple[int, int]:
    """Pick the peak (most frequent) and zero (absent) sample values.

    The zero point closest to the peak is chosen, which minimises the number
    of shifted samples and therefore the distortion.
    """
    histogram = [0] * 256
    for value in samples:
        histogram[value] += 1

    peak = max(range(256), key=lambda v: histogram[v])

    zero = None
    best_distance = 257
    for value in range(256):
        if histogram[value] == 0 and abs(value - peak) < best_distance:
            zero = value
            best_distance = abs(value - peak)
    if zero is None:
        raise ValueError(
            "The image histogram is fully saturated (every value in 0-255 "
            "occurs), so histogram-shifting has no zero point to use. Try an "
            "image with a less busy histogram."
        )
    return peak, zero


def _peak_capacity(samples: List[int], peak: int) -> int:
    return samples.count(peak)


def _embed_into_payload(
    payload: List[int], bits: List[int], peak: int, zero: int
) -> List[int]:
    """Shift the payload samples and embed ``bits`` at the peak."""
    direction = 1 if peak < zero else -1
    companion = peak + direction
    low, high = (peak, zero) if peak < zero else (zero, peak)

    result = []
    bit_iter = iter(bits)
    for sample in payload:
        if low < sample < high:
            # Make room next to the peak by shifting towards the zero point.
            result.append(sample + direction)
        elif sample == peak:
            try:
                bit = next(bit_iter)
            except StopIteration:
                result.append(peak)
            else:
                result.append(companion if bit else peak)
        else:
            result.append(sample)
    return result


def _extract_from_payload(
    payload: List[int], peak: int, zero: int, length: int
) -> Tuple[List[int], List[int]]:
    """Extract ``length`` bits and restore the original payload samples."""
    direction = 1 if peak < zero else -1
    companion = peak + direction

    bits: List[int] = []
    restored = []
    for sample in payload:
        if len(bits) < length and sample in (peak, companion):
            bits.append(0 if sample == peak else 1)
        if direction == 1:
            restored.append(sample - 1 if peak < sample <= zero else sample)
        else:
            restored.append(sample + 1 if zero <= sample < peak else sample)
    return bits, restored


def _check_mode(image: Image.Image) -> None:
    if image.mode not in ("L", "RGB", "RGBA"):
        raise ValueError(
            f"Unsupported image mode {image.mode!r}; use 'L', 'RGB' or 'RGBA'."
        )


def capacity(image: Union[str, IO[bytes], Image.Image]) -> int:
    """Return the maximum message size, in bytes, for ``image``.

    This is the size of the histogram peak minus the fixed header overhead.
    """
    img = tools.open_image(image)
    _check_mode(img)
    samples = _flatten(img)
    payload = samples[_HEADER_BITS:]
    if not payload:
        return 0
    peak, _zero = _select_peak_zero(payload)
    usable_bits = _peak_capacity(payload, peak) - _HEADER_BITS
    return max(usable_bits, 0) // 8


def hide(
    image: Union[str, IO[bytes], Image.Image],
    message: str,
    encoding: str = "UTF-8",
) -> Image.Image:
    """Hide ``message`` reversibly in ``image`` using histogram shifting.

    Returns a new :class:`PIL.Image.Image`. The original cover can later be
    recovered exactly with :func:`recover`.
    """
    img = tools.open_image(image)
    _check_mode(img)
    if encoding == "UTF-8" and any(ord(char) > 255 for char in message):
        raise ValueError(
            "The message contains characters that do not fit in one byte "
            "with the UTF-8 encoding; use the UTF-32LE encoding instead."
        )

    samples = _flatten(img)
    if len(samples) <= _HEADER_BITS:
        raise ValueError("Image is too small to hold the header.")

    header_region = samples[:_HEADER_BITS]
    payload_region = samples[_HEADER_BITS:]

    peak, zero = _select_peak_zero(payload_region)

    message_bits = [
        int(bit) for byte in tools.a2bits_list(message, encoding) for bit in byte
    ]
    # The payload also carries the original LSBs of the header samples, so the
    # header we overwrite below is itself reversible.
    saved_header_lsbs = [sample & 1 for sample in header_region]
    full_payload = saved_header_lsbs + message_bits

    available = _peak_capacity(payload_region, peak)
    if len(full_payload) > available:
        max_message_bits = max(available - _HEADER_BITS, 0)
        raise ValueError(
            "Message is too long for this image: capacity is "
            f"{max_message_bits // 8} bytes, message needs "
            f"{len(message_bits) // 8} bytes."
        )

    embedded_payload = _embed_into_payload(payload_region, full_payload, peak, zero)

    # Write the self-describing header into the LSBs of the first samples.
    header_bits: List[int] = []
    header_bits += _int_to_bits(_MAGIC, 16)
    header_bits += _int_to_bits(peak, 8)
    header_bits += _int_to_bits(zero, 8)
    header_bits += _int_to_bits(len(full_payload), 32)
    new_header = [
        tools.setlsb(sample, str(bit))
        for sample, bit in zip(header_region, header_bits)
    ]

    return _unflatten(new_header + embedded_payload, img)


def reveal(image: Union[str, IO[bytes], Image.Image], encoding: str = "UTF-8") -> str:
    """Extract the message hidden in ``image`` by :func:`hide`."""
    img = tools.open_image(image)
    samples = _flatten(img)
    header_bits = [sample & 1 for sample in samples[:_HEADER_BITS]]
    if _bits_to_int(header_bits[:16]) != _MAGIC:
        raise ValueError("No histogram-shifting payload found in this image.")
    peak = _bits_to_int(header_bits[16:24])
    zero = _bits_to_int(header_bits[24:32])
    length = _bits_to_int(header_bits[32:64])

    payload_bits, _restored = _extract_from_payload(
        samples[_HEADER_BITS:], peak, zero, length
    )
    message_bits = payload_bits[_HEADER_BITS:]

    byte_size = tools.ENCODINGS[encoding]
    characters = []
    for i in range(0, len(message_bits) - byte_size + 1, byte_size):
        characters.append(chr(_bits_to_int(message_bits[i : i + byte_size])))
    return "".join(characters)


def recover(image: Union[str, IO[bytes], Image.Image]) -> Image.Image:
    """Reconstruct the original cover image from a stego image.

    Returns an image identical, pixel-for-pixel, to the cover passed to
    :func:`hide`.
    """
    img = tools.open_image(image)
    samples = _flatten(img)
    header_bits = [sample & 1 for sample in samples[:_HEADER_BITS]]
    if _bits_to_int(header_bits[:16]) != _MAGIC:
        raise ValueError("No histogram-shifting payload found in this image.")
    peak = _bits_to_int(header_bits[16:24])
    zero = _bits_to_int(header_bits[24:32])
    length = _bits_to_int(header_bits[32:64])

    payload_bits, restored_payload = _extract_from_payload(
        samples[_HEADER_BITS:], peak, zero, length
    )
    saved_header_lsbs = payload_bits[:_HEADER_BITS]
    restored_header = [
        tools.setlsb(sample, str(bit))
        for sample, bit in zip(samples[:_HEADER_BITS], saved_header_lsbs)
    ]
    return _unflatten(restored_header + restored_payload, img)
