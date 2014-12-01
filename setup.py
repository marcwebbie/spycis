#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

__version__ = "0.0.4"

with open("README.rst") as f:
    long_description = f.read()
    ind = long_description.find("\n")
    long_description = long_description[ind + 1:]

setup(
    name='spycis',
    version=__version__,
    license='MIT',
    description='Console interface to stream websites',
    long_description=long_description,
    keywords="streaming python video download url rip convert",
    url='https://github.com/marcwebbie/spycis',
    author='Marcwebbie',
    author_email='marcwebbie@gmail.com',
    scripts=["bin/spycis", "bin/opensubtitles"],
    packages=find_packages(),
    install_requires=open('requirements.txt').readlines(),
    test_suite='tests.test',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Multimedia :: Video',
        'Topic :: Internet',
    ],
)
