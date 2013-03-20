#!/usr/bin/python
# -*- coding: utf-8 -*-

from distutils.core import setup
import os
import shutil

requires = ['PIL']


try:
    from setuptools import setup
    kw = {'zip_safe': False,
          'install_requires': requires
          }
except ImportError:
    from distutils.core import setup
    kw = {'requires': requires}




setup(
    name='Stegano',
    version='0.4',
    author='Cédric Bonhomme',
    author_email='kimble.mandel@gmail.com',
    packages=['stegano'],
    #scripts=[''],
    url='http://bitbucket.org/cedricbonhomme/stegano',
    platforms = ['Linux'],
    license='COPYING',
    description='A Python Steganography module.',
    **kw
)

print("Installing binaries")
shutil.copy2("./bin/slsb-set", "/bin/slsb-set")
shutil.copymode("./bin/slsb-set", "/bin/slsb-set")

shutil.copy2("./bin/slsb", "/bin/slsb")
shutil.copymode("./bin/slsb", "/bin/slsb")

shutil.copy2("./bin/steganalysis-parity", "/bin/steganalysis-parity")
shutil.copymode("./bin/steganalysis-parity", "/bin/steganalysis-parity")
