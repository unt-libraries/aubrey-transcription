#! /usr/bin/env python
from setuptools import setup, find_packages

setup(
    name='aubrey-transcription',
    version='3.0.0',
    packages=find_packages(exclude=['tests']),
    description='Serves up transcriptions info for Aubrey.',
    long_description='See the GitHub page for more information.',
    include_package_data=True,
    install_requires=[
        'pypairtree @ git+https://github.com/unt-libraries/pypairtree',
        'flask~=3.0.3',
    ],
    zip_safe=False,
    url='https://github.com/unt-libraries/aubrey-transcription',
    author='University of North Texas Libaries',
    author_email='mark.phillips@unt.edu',
    license='BSD',
    keywords=[
        'flask',
        'json',
        'transcript',
        'aubrey',
        'app',
        'webapp',
    ],
    classifiers=[
        'Natural Language :: English',
        'Environment :: Web Environment',
        'Framework :: Flask',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
)
