# -*- coding: utf-8 -*-
#
# This file is part of Formica released under the FreeBSD license.
# See the LICENSE for more information.
from __future__ import (print_function, division, absolute_import, unicode_literals)  # noqa

from django import forms
from django.forms.formsets import formset_factory
from django.shortcuts import render


class SimpleForm(forms.Form):
    email = forms.EmailField()
    check = forms.BooleanField()

SimpleFormset = formset_factory(SimpleForm, extra=2,
                                can_delete=True, can_order=True)


def simple_form(request):
    return render(request, 'simple.html', {
        'form': SimpleForm()
    })


def raises(request):
    return render(request, 'simple.html')


def override(request):
    return render(request, 'override.html', {
        'my_form': SimpleForm(),
        'other_form': SimpleForm(prefix='other')
    })


def table(request):
    return render(request, 'table.html', {
        'form': SimpleForm(),
        'formset': SimpleFormset()
    })


def custom(request):
    return render(request, 'custom.html', {
        'form': SimpleForm()
    })


def errors(request):
    form = SimpleForm(data={})
    form.is_valid()

    return render(request, 'simple.html', {
        'form': form
    })
