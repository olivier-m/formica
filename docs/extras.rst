======
Extras
======

Bootstrap template
==================

Formica provides a `Bootstrap <http://getbootstrap.com/>`_ ready template. All you have to do
is to call the ``formica/bootstrap/base_form.html`` template with **{% form %}** tag:

.. code-block:: django

  {% form "formica/bootstrap/base_form.html" %}
  ...
  {% endform %}

You can use the following tags (and blocks).

Basic layout
************

You can render a basic form layout with **{% fields %}** with default block:

.. code-block:: django

  {% fields "field1 field2" %}

Horizontal layout
*****************

To renders all fields with labels floating on left side, you have to use **{% fields %}** with
**horizontal** block name.

.. code-block:: django

  {% fields "field1 field2" "horizontal" %}

You can set **{{ label_cols }}** and **{{ control_cols }}** to set the grid classes for labels and controls.

With basic and horizontal style, you can also set **{{ wrapper_class }}** to add a class to
**.form-group** HTML block.

Regrouped fields
****************

To group all fields on a single line, use **{{ fields }}** with **regrouped** block name.
You can set a **{{ label }}** variable to add a label.

.. code-block:: django

  {% fields "field1 field2" "regrouped" label="optional label" %}

Template filters
================

Formica provides template filters mostly borrowed from
`django-crispy-forms <https://github.com/maraujop/django-crispy-forms>`_.

\|is_input
**********

Returns **True** if field's widget is a ``<input>`` tag, except checkboxe, radio or file.

\|is_textarea
*************

Returns **True** if field's widget is a textarea (``forms.Textarea``).

\|is_select
***********

Returns **True** if field's widget is a select box.

\|is_checkbox
*************

Returns **True** if field's widget is a checkbox (``forms.CheckboxInput``).

\|is_password
*************

Returns **True** if field's widget is a password input (``forms.PasswordInput``).

\|is_radioselect
****************

Returns **True** if field's widget is a radio select choice (``forms.RadioSelect``).

\|is_checkboxselectmultiple
***************************

Returns **True** if field's widget is a multiple checkbox select (``forms.CheckboxSelectMultiple``).

\|is_file
*********

Return **True** if field's widget is a file input (``forms.FileInput``).

\|any_field_error
*****************

This filter applies on a field list and returns **True** if any one of them has errors.

\|any_field_required
********************

This filter applies on a field list and returns **True** if any one of them is required.


.. _demo:

Demonstration project
=====================

Formica provides a demonstration project, allowing you to see how it looks and how it works with
various templates. Here's how to run it.

First, clone the project (prefer a virtual environment)::

  git clone https://github.com/olivier-m/formica.git

Then install formica::

  cd formica
  pip install -e .

Run the demonstration project::

  cd demo-project
  python manage.py runserver

You'll find all needed sources in **demo-project** directory.
