=====================
Templates and recipes
=====================

Provided templates
==================

formica/base_form.html
**********************

This is the base Formica template. It produces a pretty decent form with a **div** element for
each form, shows errors, adds CSRF prevention. It tries to be simple and covers all needs but I'm
sure you will change it to match your CSS.
:ref:`Customisation and contributions<contrib>` for CSS frameworks are welcome :)

Here is an example of code produced with this template:

Template:
---------

.. code-block:: django

  {% form "formica/base_form.html" wrapper_class="horizontal" %}
    {% fields email_field__size=30 email_field__wrapper_class="" %}
  {% endform %}

Render to:
----------

.. code-block:: html

  <input type='hidden' name='csrfmiddlewaretoken' value='xxxxx' />
  <div class="field horizontal ">
    <div class="field-content">
      <input id="id_boolean_field" name="boolean_field" type="checkbox" />
      <label for="id_boolean_field">Boolean Field</label>
    </div>
  </div>

  <div class="field horizontal required ">
    <label for="id_date_field" class="required">Date Field</label>
    <div class="field-content">
      <input id="id_date_field" name="date_field" type="date" />
      <span class="hint">Enter date please</span>
    </div>
  </div>

  <div class="field required ">
    <label for="id_email_field" class="required">Email Field</label>
    <div class="field-content">
      <input id="id_email_field" name="email_field" type="email" size="30" />
    </div>
  </div>

Using this template, here are some interesting variables:

- **{{ wrapper_class }}**: adds classes to **div.field** element (used by **field** block)
- **{{ with_csrf }}**: adds CSRF field (true by default)


formica/table_form.html
***********************

This template allows you to render a form as a table with each field in a column and labels in
table header. Here is an example:

Template:
---------

.. code-block:: django

  {% form "formica/table_form.html" name__placeholder="placeholder" %}
    {% fields name__size=8 %}
  {% endform %}

Render to:
----------

.. code-block:: html

  <input name="csrfmiddlewaretoken" value="xxxxx" type="hidden">
  <table class="form-table">
    <thead>
    <tr>
      <th class="required">
        <label for="id_qty" class="required">Qty.</label>
      </th>
      <th class="required">
        <label for="id_name" class="required">Name</label>
      </th>
      <th class="">
        <label for="id_date">Date</label>
      </th>
      <th class="required">
        <label for="id_mch" class="required">Pick one</label>
      </th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td class="field "><input id="id_qty" name="qty" type="number"></td>
      <td class="field "><input id="id_name" maxlength="40" name="name"
        placeholder="placeholder" size="8" type="text"></td>
      <td class="field "><input id="id_date" name="date" type="text"></td>
      <td class="field "><select id="id_mch" name="mch">
        <option value="1">Dogs</option>
        <option value="2">Cats</option>
        <option value="3">Birds</option>
      </select></td>
    </tr>
  </tbody>
  </table>


Formsets
========

Formsets are easy to handle with Formica, including tabular formset layouts.

The easiest way, using a for loop (without management form nor error support):

.. code-block:: django

  {% for form in formset %}
    {# Look how we render CSRF field on first iteration only #}
    {% form "formica/base_form.html" with_csrf=forloop.first %}
      {% fields %}
    {% endform %}
  {% endfor %}

The ``formica/table_form.html`` template provides some helpers to render a formset in a table
with labels in header and a row for each form. Here's how:

.. code-block:: django

  {# Use the formset var by default, pass formset= to change it #}
  {% use "formica/table_form.html" "table_formset" name__size=8 %}{% enduse %}

The **table_formset** block from this template places the tag contents just after the **<table>**
tag. Thus you can do things like adding a **caption** or **colgroup** elements:

.. code-block:: django

  {% use "formica/table_form.html" %}
    <caption>Formset</caption>
  {% enduse %}

It becomes:

.. code-block:: html

  <table class="form-table">
    <caption>Formset</caption>
    <!-- ... -->
  </table>

.. _contrib:

Customize templates
===================

You need only 3 templates blocks to render templates with Formica. Here are their descriptions and
context they receive.

form
****

The main block. Called by `form`_ tag. This is the place to render CSRF protection, errors and the
tag contents. It receives the following variables:

- **{{ contents }}**: The **{% form %}** tag content
- **{{ form }}**: The form instance

fields
******

This block is very simple, it receives the **{{ form }}** variable from **{% form %}** tag and a
**{{ fields }}** variable containing form field instances. The basic implementation is:

.. code-block:: django

  {% block fields %}
  {% for field in fields %}
    {% field field %}
  {% endfor %}
  {% endblock fields %}

You can extend it to add a fieldset element each time you call **{% fields %}** tag.
Here's a snippet:

.. code-block:: django

  {% extends "formica/base_form.html" %}

  {% block fields %}
  <fieldset>{% if legend %}<legend>{{ legend }}</legend>{% endif %}
  {{ block.super }}
  </fieldset>
  {% endblock %}

  {# called with : {% fields legend="My Fieldset" %} #}

field
*****

This block renders the field itself. This is where you usually make the hard work to render your
HTML tags. It receives the following template variables:

- **{{ field }}**: The field instance
- **{{ form }}**: The form instance (comming from **{% form %}** tag)
