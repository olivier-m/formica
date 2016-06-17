# -*- coding: utf-8 -*-
from __future__ import (print_function, division, absolute_import, unicode_literals)  # noqa

from django.conf.urls import url

from . import views

urlpatterns = (
    url(r'^$', views.home, name='home'),
    url(r'^default$', views.form_view, name='default',
        kwargs={'template_name': 'default.html'}),
    url(r'^bootstrap$', views.form_view, name='bootstrap',
        kwargs={'template_name': 'bootstrap.html'}),
)
