# -*- coding: utf-8 -*-
#
# This file is part of Formica released under the FreeBSD license.
# See the LICENSE for more information.
from setuptools import setup

# Get app version
with open('formica/version.py', 'rb') as fp:
    g = {}
    exec(fp.read(), g)
    version = g['__version__']


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
        'django>=1.4',
    ],
    packages=['formica', 'formica.templatetags'],
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
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
