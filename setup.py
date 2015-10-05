#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import shutil

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

packages = [
    'stegano',
    'stegano.exif',
    'bin'
]

requires = ['pillow']

with open('README.md', 'r') as f:
    readme = f.read()

setup(
    name='Stegano',
    version='0.4.2',
    author='Cédric Bonhomme',
    author_email='cedric@cedricbonhomme.org',
    packages=packages,
    include_package_data=True,
    #scripts=[''],
    url='https://bitbucket.org/cedricbonhomme/stegano',
    description='A Python Steganography module.',
    long_description=readme,
    platforms = ['Linux'],
    license='GPLv3',
    install_requires=requires,
    zip_safe=False,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Topic :: Utilities",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)"
    ]
)

if sys.argv[-1] == "install":
    print("Installing binaries")
    shutil.copy2("./bin/slsb-set", "/bin/slsb-set")
    shutil.copymode("./bin/slsb-set", "/bin/slsb-set")

    shutil.copy2("./bin/slsb", "/bin/slsb")
    shutil.copymode("./bin/slsb", "/bin/slsb")

    shutil.copy2("./bin/steganalysis-parity", "/bin/steganalysis-parity")
    shutil.copymode("./bin/steganalysis-parity", "/bin/steganalysis-parity")
