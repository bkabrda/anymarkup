#!/usr/bin/env python3
# -*- coding: utf-8 -*-

try:
    from setuptools import setup, find_packages
except:
    from distutils.core import setup, find_packages

setup(
    name='anymarkup',
    version='0.0.1',
    description='Load any markup document to Python structure',
    long_description=''.join(open('README.rst').readlines()),
    keywords='xml, yaml, json, ini',
    author='Slavek Kabrda',
    author_email='slavek.kabrda@gmail.com',
    license='BSD',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        ]
)
