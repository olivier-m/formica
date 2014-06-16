Overview
========

Rendering forms with Django could be painful and not very rewarding. There are some nice solutions
arround like `django-floppyforms <http://django-floppyforms.readthedocs.org/en/latest/>`_ or
`django-crispy-forms <https://github.com/maraujop/django-crispy-forms>`_ but you may want
something a bit less complex.

Formica design is heavily based on `Formulation <https://github.com/funkybob/formulation/>`_, a very
lightweight, yet powerful, solution based on template blocks. All credits should go to
`Curtis Maloney <https://github.com/funkybob>`_ for this impressive and simple idea.

A simple example
================

Say we have a form somewhere and want to render it in a template.

::

  from django import forms
  class MyForm(forms.Form):
    email = forms.EmailField(label='Email')
    check = forms.BooleanField(label='I really love spam', required=False)

Render the form is as simple as::

  {% load formica %}

  <form method="post">
    {% form "formica/base_form.html" %}
      {% fields %}
    {% endform %}

    <p><input type="submit" value="save" /></p>
  </form>

Pretty cool isn't it?
Read the `documentation <http://pythonhosted.org/formica>`_ to learn more.

Sources & license
=================

Formica sources are hosted on Gihub:
https://github.com/olivier-m/formica

Formica is released under the
`FreeBSD license <http://www.freebsd.org/copyright/freebsd-license.html>`_.
