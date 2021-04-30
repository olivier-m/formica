=======
Formica
=======

Contents:

.. toctree::
  :maxdepth: 2

  usage
  templates
  extras

Overview
========

Rendering forms with Django can be painful and not very rewarding. There are some nice solutions
arround like `django-floppyforms <http://django-floppyforms.readthedocs.org/en/latest/>`_ or
`django-crispy-forms <https://github.com/maraujop/django-crispy-forms>`_ but you may want
something a bit less complex.

Formica design is heavily based on `Formulation <https://github.com/funkybob/formulation/>`_, a very
lightweight, yet powerful, solution based on template blocks. All credits should go to
`Curtis Maloney <https://github.com/funkybob>`_ for this impressive and simple idea.

.. note::

  If you're in a hurry and just want to see how it looks and how it works, there's a
  :ref:`demonstration project <demo>` for you.

A simple example
================

Say we have a form somewhere and want to render it in a template.

.. code-block:: python

  from django import forms
  class MyForm(forms.Form):
    email = forms.EmailField(label='Email')
    check = forms.BooleanField(label='I really love spam', required=False)

Rendering the form is as simple as:

.. code-block:: django

  {% load formica %}

  <form method="post">
    {% form "formica/base_form.html" my_form %}
      {% fields %}
    {% endform %}

    <p><input type="submit" value="save" /></p>
  </form>

Pretty cool isn't it? Now let's dive into more complex and :doc:`real life usages<usage>`.

Changes
=======

version 1.2.1 - 2014-08-22
==========================

- Django 1.7 compatibility

version 1.2 - 2014-08-21
========================

- Changes in default template blocks
- Minor fixes for Bootstrap

version 1.1 - 2014-06-19
************************

- Bootstrap template
- New filters (is_input, is_textarea, is_select)
- Added an context **attrs** variable in **{% field %}** tag.
- Demonstration project
- Stylesheet for default template

version 1.0 - 2014-06-16
************************

- Initial release.

Sources & license
=================

Formica sources are hosted on Github:
https://github.com/olivier-m/formica

Formica is released under the
`FreeBSD license <http://www.freebsd.org/copyright/freebsd-license.html>`_.
