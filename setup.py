 #!/usr/bin/python
# -*- coding: utf-8 -*-

from distutils.core import setup
import os

setup(
    name='Stegano',
    version='0.3',
    author='Cédric Bonhomme',
    author_email='kimble.mandel@gmail.com',
    packages=['stegano'],
    #scripts=[''],
    url='http://bitbucket.org/cedricbonhomme/stegano',
    platforms = ['Linux'],
    license='COPYING',
    description='A Python Steganography module.',
)
