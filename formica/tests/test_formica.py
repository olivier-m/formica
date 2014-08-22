# -*- coding: utf-8 -*-
#
# This file is part of Formica released under the FreeBSD license.
# See the LICENSE for more information.
from __future__ import (print_function, division, absolute_import, unicode_literals)
import os.path

from django.template import TemplateSyntaxError
from django.test import TestCase
from django.test.utils import override_settings

try:
    from bs4 import BeautifulSoup as BS
except ImportError:
    raise Exception('You should install BeautifulSoup to run tests.')


TEMPLATE_DIRS = (os.path.join(os.path.dirname(__file__), 'templates'),)


@override_settings(TEMPLATE_DIRS=TEMPLATE_DIRS)
class FormicaTestCase(TestCase):
    urls = 'formica.tests.urls'

    def assertTag(self, d, selector, count=1):
        self.assertEqual(count, len(d.select(selector)))

    def assertAttr(self, d, selector, name, value):
        tag = d.select(selector)
        if len(tag) != 1:
            raise AssertionError('Found 0 or more than one tag.')

        self.assertEqual(tag[0].attrs[name], value)

    def test_simple(self):
        r = self.client.get('/')
        d = BS(r.content)

        self.assertTag(d, 'input#id_email')
        self.assertTag(d, 'div.form-field > label[for="id_email"]')
        self.assertTag(d, 'input#id_check')
        self.assertTag(d, 'div.form-field > div.field-content > label[for="id_check"]')

    def test_raise(self):
        self.assertRaises(TemplateSyntaxError, self.client.get, '/raises')

    def test_override(self):
        r = self.client.get('/override')
        d = BS(r.content)

        self.assertTag(d, 'input#id_email')
        self.assertTag(d, 'input#id_check')
        self.assertTag(d, 'input#id_other-email')
        self.assertTag(d, 'input#id_other-check')

        self.assertTag(d, '#my_form div.form-field', 2)
        self.assertTag(d, '#my_form div.form-field.wrapped')
        self.assertTag(d, '#my_form input[name="csrfmiddlewaretoken"]')

        self.assertTag(d, '#other_form div.form-field', 2)
        self.assertAttr(d, '#other_form input#id_other-email', 'size', '40')
        self.assertTag(d, '#other_form div.form-field.wrapped input#id_other-email')
        self.assertAttr(d, '#other_form input#id_other-check', 'class', ['checkbox'])
        self.assertAttr(d, '#other_form input#id_other-check', 'title', 'check title')
        self.assertTag(d, '#other_form input[name="csrfmiddlewaretoken"]', 0)

        self.assertEqual('', d.select('#void')[0].text)

    def test_table(self):
        r = self.client.get('/table')
        d = BS(r.content)

        self.assertTag(d, '#form thead > tr > th > label[for="id_email"]')
        self.assertTag(d, '#form thead > tr > th > label[for="id_check"]')
        self.assertTag(d, '#form tbody > tr > td.form-field > input#id_email')
        self.assertTag(d, '#form tbody > tr > td.form-field > input#id_check')

        self.assertTag(d, '#formset thead')
        self.assertTag(d, '#formset tbody > tr', 2)
        self.assertAttr(d, '#formset > div > input#id_form-TOTAL_FORMS', 'value', '2')
        self.assertTag(d, '#formset tbody > tr > td.form-field > input#id_form-0-email')
        self.assertTag(d, '#formset tbody > tr > td.form-field > input#id_form-1-check')
        self.assertTag(d, '#formset tbody > tr > td.form-field > input#id_form-1-ORDER')
        self.assertTag(d, '#formset tbody > tr > td.form-field > input#id_form-1-DELETE')

    def test_custom(self):
        r = self.client.get('/custom')
        d = BS(r.content)

        self.assertTag(d, '#fields > div.void')

        self.assertTag(d, '#field div.super-wrapper > div.form-field input#id_email')
        self.assertTag(d, '#field div.super-wrapper > div.form-field input#id_check')

    def test_errors(self):
        r = self.client.get('/errors')
        d = BS(r.content)

        self.assertTag(d, 'body > div.form-errors > strong')
        self.assertTag(d, 'div.form-field > ul.errorlist > li', 2)
