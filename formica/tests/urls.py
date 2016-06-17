# -*- coding: utf-8 -*-
#
# This file is part of Formica released under the FreeBSD license.
# See the LICENSE for more information.
from __future__ import (print_function, division, absolute_import, unicode_literals)  # noqa

from django.conf.urls import url

from formica.tests import views

urlpatterns = (
    url(r'^$', views.simple_form, name='simple_form'),
    url(r'^raises$', views.raises, name='raises'),
    url(r'^override$', views.override, name='override'),
    url(r'^table$', views.table, name='table'),
    url(r'^custom$', views.custom, name='custom'),
    url(r'^errors$', views.errors, name='errors'),
)
