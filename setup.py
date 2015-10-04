#!/usr/bin/python
# -*- coding: utf-8 -*-

import setuptools
import os
import shutil

from distutils.core import setup, Extension

requires = ['pillow']

kw = {'install_requires': requires}

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='Stegano',
    version='0.4',
    author='Cédric Bonhomme',
    author_email='cedric@cedricbonhomme.org',
    packages=['stegano'],
    #scripts=[''],
    url='https://bitbucket.org/cedricbonhomme/stegano',
    long_description=read('README.md'),
    platforms = ['Linux'],
    license='GPLv3',
    description='A Python Steganography module.',
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Topic :: Utilities",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)"
    ],
    **kw
)

print("Installing binaries")
shutil.copy2("./bin/slsb-set", "/bin/slsb-set")
shutil.copymode("./bin/slsb-set", "/bin/slsb-set")

shutil.copy2("./bin/slsb", "/bin/slsb")
shutil.copymode("./bin/slsb", "/bin/slsb")

shutil.copy2("./bin/steganalysis-parity", "/bin/steganalysis-parity")
shutil.copymode("./bin/steganalysis-parity", "/bin/steganalysis-parity")
