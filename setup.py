#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

__version__ = "0.0.1-dev6"

long_description = """Spycis is a python console interface to stream websites
"""

setup(
    name='spycis',
    version=__version__,
    license='MIT',
    description='Console interface to stream websites',
    long_description="Spycis is a python console interface to stream websites",
    keywords=long_description,
    url='https://github.com/marcwebbie/spycis',
    author='Marcwebbie',
    author_email='marcwebbie@gmail.com',
    scripts=["bin/spycis", "bin/pyddicted"],
    packages=find_packages(),
    install_requires=open('requirements.pip').readlines(),
    test_suite='tests.test',
    classifiers=[
        'Development Status :: Alpha',
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
