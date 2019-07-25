#!/usr/bin/python3
from setuptools import setup, find_packages

__author__ = 'aelkikhia'

setup(
    name='pyduel_engine',
    version='0.1',
    description='Duels engine written in python',
    author='Taz El-Kikhia',
    author_email='aelkikhia@gmail.com',
    tests_require=[
        'pycodestyle',
        'mock',
        'testtools',
        'pylint',
        'pytest',
        'coverage'
    ],
    install_requires=[
        'flask',
        'flask-cors',
        'Flask-RESTful',
        'jsonschema',
        'python-json-logger',
        'python-dotenv',
        'requests',
        'pyyaml'
    ],
    test_suite='nose.collector',
    zip_safe=False,
    include_package_data=True,
    packages=find_packages(exclude=['ez_setup'])
)
