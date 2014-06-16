# -*- coding: utf-8 -*-
#
# This file is part of Formica released under the FreeBSD license.
# See the LICENSE for more information.
from __future__ import (print_function, division, absolute_import, unicode_literals)

from setuptools import setup, find_packages

# Get app version
with open('formica/version.py', 'rb') as fp:
    g = {}
    exec(fp.read(), g)
    version = g['__version__']

# Get package list and make app name mapping
packages = find_packages(exclude=['*.tests'])


# Read README file
def readme():
    with open('README.rst', 'r') as fp:
        return fp.read()


# Setup
setup(
    name='formica',
    version=version,
    description='Django form rendering helpers',  # Change it for a better description :)
    author='Olivier Meunier',
    author_email='olivier@neokraft.net',
    license='FreeBSD',
    url='http://pythonhosted.org/formica',
    long_description=readme(),
    keywords='django forms templates',
    install_requires=[
        'django',
    ],
    packages=packages,
    include_package_data=True,
    zip_safe=False,
    test_suite='tests.runtests',
    tests_require=[
        'pyquery',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
