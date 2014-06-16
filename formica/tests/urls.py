# -*- coding: utf-8 -*-
#
# This file is part of Formica released under the FreeBSD license.
# See the LICENSE for more information.
from __future__ import (print_function, division, absolute_import, unicode_literals)

from django.conf.urls import patterns, url


urlpatterns = patterns(
    'formica.tests.views',

    url(r'^$', 'simple_form', name='simple_form'),
    url(r'^raises$', 'raises', name='raises'),
    url(r'^override$', 'override', name='override'),
    url(r'^table$', 'table', name='table'),
    url(r'^custom$', 'custom', name='custom'),
    url(r'^errors$', 'errors', name='errors'),
)
