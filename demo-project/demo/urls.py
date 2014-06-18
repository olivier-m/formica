# -*- coding: utf-8 -*-
from __future__ import (print_function, division, absolute_import, unicode_literals)

from django.conf.urls import patterns, url

urlpatterns = patterns(
    'demo.views',
    url(r'^$', 'home', name='home'),
    url(r'^default$', 'form_view', name='default', kwargs={'template_name': 'default.html'}),
    url(r'^bootstrap$', 'form_view', name='bootstrap', kwargs={'template_name': 'bootstrap.html'}),
)
