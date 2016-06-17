# -*- coding: utf-8 -*-
#
# This file is part of Formica released under the FreeBSD license.
# See the LICENSE for more information.
from __future__ import (print_function, division, absolute_import, unicode_literals)

import sys
import warnings

warnings.simplefilter('always')

from django.conf import settings

try:
    from django.utils.functional import empty
except ImportError:
    empty = None


APPS = (
    'formica',
)


def setup_test_environment():
    # reset settings
    settings._wrapped = empty

    settings_dict = {
        'DATABASES': {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
            },
        },
        'INSTALLED_APPS': APPS,
        'MIDDLEWARE_CLASSES': (
            'django.middleware.common.CommonMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.middleware.clickjacking.XFrameOptionsMiddleware',
        ),
        'ROOT_URLCONF': '',
        'TEMPLATE_CONTEXT_PROCESSORS': [
            "django.template.context_processors.debug",
            "django.template.context_processors.i18n",
            "django.template.context_processors.media",
            "django.template.context_processors.static",
            "django.template.context_processors.tz",
            "django.contrib.messages.context_processors.messages"
        ]
    }

    settings.configure(**settings_dict)


def runtests():
    setup_test_environment()

    try:
        import django
        from django.test.runner import DiscoverRunner as TestRunner

        if hasattr(django, 'setup'):  # Django >= 1.7
            django.setup()
        test_args = ['formica.tests']
    except ImportError:  # Django < 1.6
        from django.test.simple import DjangoTestSuiteRunner as TestRunner
        test_args = ['formica']

    runner = TestRunner(verbosity=1, interactive=True, failfast=False)
    failures = runner.run_tests(test_args)
    sys.exit(failures)

if __name__ == '__main__':
    runtests()
