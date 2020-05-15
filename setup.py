#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup  # type: ignore

setup(
    name='pyeupi',
    version='1.1',
    author='Raphaël Vinot',
    author_email='raphael.vinot@circl.lu',
    maintainer='Raphaël Vinot',
    url='https://github.com/CIRCL/PyEUPI',
    description='Python API for the European Union anti-phishing initiative.',
    packages=['pyeupi'],
    entry_points={"console_scripts": ["pyeupi = pyeupi:main"]},
    classifiers=[
        'License :: OSI Approved :: BSD License',
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Telecommunications Industry',
        'Programming Language :: Python :: 3',
        'Topic :: Security',
        'Topic :: Internet',
    ],
    install_requires=['requests'],
    package_data={'': ['*.md', '*.rst', 'LICENSE']},
)
