#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(

    name='pandangas',

    version='0.0.1',

    packages=find_packages(),

    author="Pablo Puerto",

    author_email="pablo.puerto@mines-albi.fr",

    description="Natural Gas network design and simulation tool, largely inspired by PandaPower",

    long_description=open('README.md').read(),

    install_requires=[
        "networkx >= 2",
        "pandas >= 0.25",
        "thermo >= 0.1.39",
        "fluids >= 0.1.75",
        "scipy >= 1.3.3",
        "numpy >= 1.17.4"
    ],

    include_package_data=True,

    url='',

    classifiers=[
        "Natural Language :: English",
        "Operating GraphCreator :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Topic :: Simulation",
    ]

)
