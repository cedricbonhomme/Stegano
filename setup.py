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
    'stegano.red',
    'stegano.exifHeader',
    'stegano.lsb',
    'stegano.lsbset',
    'stegano.steganalysis'
]

scripts = [
    'bin/lsb',
    'bin/lsb-set',
    'bin/stegano-red',
    'bin/steganalysis-parity',
    'bin/steganalysis-statistics'
]

requires = ['pillow', 'piexif', 'crayons']

with open('README.rst', 'r') as f:
    readme = f.read()
with open('CHANGELOG.rst', 'r') as f:
    changelog = f.read()

setup(
    name='Stegano',
    version='0.6.9',
    author='Cédric Bonhomme',
    author_email='cedric@cedricbonhomme.org',
    packages=packages,
    include_package_data=True,
    scripts=scripts,
    url='https://github.com/cedricbonhomme/Stegano',
    description='A pure Python Steganography module.',
    long_description=readme + '\n|\n\n' + changelog,
    platforms = ['Linux'],
    license='GPLv3',
    install_requires=requires,
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Topic :: Security',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)'
    ]
)
