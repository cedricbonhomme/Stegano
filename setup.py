#!/usr/bin/python
# -*- coding: utf-8 -*-
import codecs
import os

from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))

packages = [
    'stegano',
    'stegano.red',
    'stegano.exifHeader',
    'stegano.lsb',
    'stegano.lsbset',
    'stegano.steganalysis'
]

scripts = [
    'bin/stegano-lsb',
    'bin/stegano-lsb-set',
    'bin/stegano-red',
    'bin/stegano-steganalysis-parity',
    'bin/stegano-steganalysis-statistics'
]

requires = ['pillow', 'piexif', 'crayons']

with codecs.open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    readme = f.read()
with codecs.open(os.path.join(here, 'CHANGELOG.rst'), encoding='utf-8') as f:
    changelog = f.read()

setup(
    name='Stegano',
    version='0.9.0',
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
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)'
    ]
)
