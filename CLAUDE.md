# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Stegano is a pure Python steganography module that provides multiple techniques for hiding messages in images and audio files. The codebase is structured around independent steganography techniques, each with a `hide()` and `reveal()` interface.

## Development Commands

### Testing
```bash
# Run all tests
python -m unittest discover -v

# Run a single test file
python -m unittest tests.test_lsb -v

# Run a specific test case
python -m unittest tests.test_lsb.TestLSB.test_hide_and_reveal -v
```

### Type Checking
```bash
# Run mypy static type checker
mypy stegano
```

### Code Quality
```bash
# Run pre-commit hooks manually
pre-commit run --all-files

# Install pre-commit hooks
pre-commit install
```

### Building Documentation
```bash
cd docs
pip install -r requirements.txt
make html
```

## Architecture

### Core Steganography Techniques

The module provides four main steganography techniques, each in its own submodule:

1. **LSB (Least Significant Bit)** - `stegano/lsb/`
   - Primary technique using pixel LSB manipulation
   - Supports custom generators for pixel selection (see Generators below)
   - Main API: `lsb.hide(image, message, generator=None, shift=0)` and `lsb.reveal(encoded_image, generator=None, shift=0)`

2. **Red Channel** - `stegano/red/`
   - Uses only the red channel of RGB pixels
   - Simpler but more limited (max 254 characters)
   - Main API: `red.hide(input_image, message)` and `red.reveal(input_image)`

3. **EXIF Headers** - `stegano/exifHeader/`
   - Embeds messages in JPEG/TIFF EXIF metadata
   - Uses base64 encoding and compression
   - Main API: `exifHeader.hide(input_image_file, img_enc, secret_message=None, secret_file=None)` and `exifHeader.reveal(input_image_file)`

4. **WAV Audio** - `stegano/wav/`
   - Hides messages in uncompressed WAV audio files
   - Uses LSB of PCM samples
   - Main API: `wav.hide(input_file, message, output_file)` and `wav.reveal(input_file)`

### Generators System

The LSB technique supports pluggable generators (in `stegano/lsb/generators.py`) that determine which pixels are used for encoding. This makes steganalysis more difficult by scattering the message according to mathematical sequences:

- `identity()` - Sequential pixels (default)
- `eratosthenes()` - Prime numbers via Sieve of Eratosthenes
- `fibonacci()` - Fibonacci sequence
- `mersenne()` - Mersenne primes
- `triangular_numbers()` - Triangular numbers
- `fermat()` - Fermat numbers
- `ackermann(m)` - Ackermann function
- `LFSR(m)` - Linear-feedback shift register
- `shi_tomashi(image_path, ...)` - OpenCV corner detection

The same generator must be used for both hiding and revealing.

### Shared Utilities

`stegano/tools.py` contains shared classes and utilities:
- `Hider` class - Handles message encoding into images
- `Revealer` class - Handles message extraction from images
- Bit manipulation functions (`setlsb`, `a2bits`, `a2bits_list`)
- Image handling (`open_image`)

### Steganalysis Module

`stegano/steganalysis/` provides tools to detect steganography:
- `parity.py` - LSB parity detection
- `statistics.py` - Statistical analysis

### Console Scripts

`stegano/console/` contains CLI entry points defined in `pyproject.toml`:
- `stegano-lsb` - LSB technique CLI
- `stegano-red` - Red channel technique CLI
- `stegano-steganalysis-parity` - Parity analysis CLI
- `stegano-steganalysis-statistics` - Statistical analysis CLI

## Key Patterns

### Consistent API Design
All steganography techniques follow the pattern:
- `hide(input, message, [options]) -> output` - Returns PIL Image or writes to file
- `reveal(input, [options]) -> str` - Returns decoded message

### Image Handling
- Uses PIL (Pillow) for image operations
- LSB techniques work with RGB/RGBA modes (auto-conversion available)
- Red channel technique requires RGB
- Images are opened via `tools.open_image()` which accepts file paths, file objects, or PIL Images

### Encoding
- Default encoding is UTF-8 (8 bits per character)
- UTF-32LE (32 bits) also supported
- Message length is encoded in the output for extraction

## Test Structure

Tests are in `tests/` directory:
- Sample files in `tests/sample-files/`
- Expected output images in `tests/expected-results/`
- Each technique has its own test file (e.g., `test_lsb.py`, `test_red.py`)
- Generators have dedicated tests in `test_generators.py`
