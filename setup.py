#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='anymarkup',
    version='0.1.1',
    description='Parse/serialize any markup format',
    long_description=''.join(open('README.rst').readlines()),
    keywords='xml, yaml, json, ini',
    author='Slavek Kabrda',
    author_email='slavek.kabrda@gmail.com',
    license='BSD',
    packages=['anymarkup'],
    install_requires=open('requirements.txt').read().splitlines(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        ]
)
