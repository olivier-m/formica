=============
Formica usage
=============

Installation
============

Formica is tested with Django version 1.4 to 1.6 and with Python version 2.6, 2.7, 3.2, 3.3 and 3.4.

Install Formica package from pypi using Pip (or wathever you like):

::

  pip install formica

Then, add ``formica`` to your ``INSTALLED_APPS`` setting. You're now ready to use all these cool
template tags!

Template tags
=============

{% form %}
----------

**{% form %}** is the main template tag you use when rendering a single form. It basically loads a
template, sets a new context and render what's inside the tag. If we have a form named
**{{ my_form }}** in our website template and we want to render it using ``formica/base_form.html``
template, we add this in our website template:

.. code-block:: django

  {% load formica %}

  {% form "formica/base_form.html" my_form %}
    {# render all form fields #}
    {% fields %}
  {% endform %}

The first **{% form %}** tag argument is the template name and is required. The second argument is
the form instance you want to use in this tag. If you don't provide it, the context variable
**{{ form }}** will be used by default (provided it exists).

You can pass :ref:`keyword arguments <kwargs>` to this tag.

{% fields %}
------------

Inside a `{% form %}`_ tag, **{% fields %}** allows you to render fields. It takes on optional field
list in order to let you choose which fields to render and/or their order. Here is an example:

.. code-block:: django

  {% load formica %}

  {# use existing "form" variable in context #}
  {% form "formica/base_form.html" %}
    {# render only the fields "name" and "email" #}
    {% fields "name, email" %}

    {# render all other fields except "name" and "email" #}
    {% fields "-name, -email" %}
  {% endform %}

As you can see, you can specify which fields to display or to hide (using minus sign before the
name). You can use any combination you like. If the field list argument is not provided or is empty,
all form fields are rendered.

As a second argument **{% fields %}** tag takes an optional block name which default value is
**fields**. Here is a example:

.. code-block:: django

  {% load formica %}

  {# We define a block here for documentation purpose but it would be #}
  {# more convenient to put it in a specific template.                #}
  {% block my_fields %}
    {% for field in fields %}
      <p>Hurray, a field!</p>
      {% field field %}
    {% endfor %}
  {% endblock %}

  {% form "formica/base_form.html" %}
    {# render all fields using our custom block #}
    {% fields "" "my_fields" %}
  {% endform %}

Did you notice how we use an empty value as first ``fields`` argument to render all fields?

You can pass :ref:`keyword arguments <kwargs>` to this tag but we'll see that later.

{% field %}
-----------

**{% field %}** tag is responsible for rendering a form field (I'm sure you're thrilled by such a
bold tag name). It takes the field name or instance as a first argument. As a second argument, it
takes an optional block name which default value is **field**. Here is an example:

.. code-block:: django

  {% load formica %}

  {# use default "form" variable #}
  {% form "formica/base_form.html" %}
    {# render the field named "email" #}
    {% field "email" %}

    {# render the first field in form (illustration purpose only) #}
    {% field form.0 %}

    {# render the field named "name" with a custom block "custom_field" #}
    {% field "name" "custom_field" %}
  {% endform %}

That was easy. As with other fields, you can pass keywords arguments to this tag but in this case
you can do more. Each keyword argument passed to **{% field %}** tag, provided it is a whole word or
starts with **data_**, would be added to the field widget attributes. Here is an example:

.. code-block:: django

  {% load formica %}

  {# use default "form" variable #}
  {% form "formica/base_form.html" %}
    {# sets size and placeholder #}
    {% field "email" size=40 placeholder="email" %}

    {# sets data argument and class #}
    {% field "name" data_foo="bar" class="name-input" %}

    {# sets nothing (wrong format) #}
    {% field "firstname" wrapper_class="inline" %}
  {% endform %}

In this example, the first two fields widget (HTML tag) have new attributes. The last field won't
have any attribute because **wrapper_class** is not in a correct format to become a widget
attribute. However, this argument is transmitted in context for the block rendering the field.
Jump to :ref:`keyword arguments <kwargs>` section to learn more about it.

{% useblock %}
--------------

This tag allows you to "call" a block (see it like a macro). It takes a required block name as a
first argument and keyword arguments. Here is an example:

.. code-block:: django

  {% load formica %}

  {% form "formica/base_form.html" %}
    {% useblock "fields" fields=form %}
  {% endform %}

This is an interesting example because it works. In "base_form" template, the **fields** block
iterates on **{{ fields }}** variable and call the **{% field %}** tag. In this case we call this
block saying **{{ fields }}** is **{{ form }}** (which allows fields iteration).

You can see this tag as an **{% include %}** tag for blocks allowing context override.

{% use %}
---------

**{% use %}** is like the `{% form %}`_ tag except it's not form centric. (**{% form %}** is
actually a child of this tag). It takes a required template name and block name and, any optional
keyword arguments (overriding context but I think you get it). Here is an example:

.. code-block:: django

  {% load formica %}

  {% use "my-app/blocks.html" "shiny" var1=2 %}
    <p>Tag content</p>
  {% enduse %}

Provided you have a **shiny** block in ``my-app/blocks.html``, this tag will render the content of
the block using the content of the tag as **{{ contents }}** variable. Here is the block definition
and the result of this example:

.. code-block:: django

  {% block shiny %}
  <div>{{ contents }} <p>{{ var1 }}</p></div>
  {% endblock %}

The result:

.. code-block:: html

  <div><p>Tag content</p> <p>2</p></div>

The `{% form %}`_ tag works in the same way except we force the block name to be **form**.

{% set %}
---------

As you will see later, you can add many keyword arguments to the previous template tags. For some
reason, you can't write a template tag on multiple lines:

.. code-block:: django

  {% load formica %}

  {# This will raise a syntax error #}
  {% form "formica/base_form.html"
    name__size=40 name__class="name"
    email__class="email"
  %}
  {% endform %}

If you have a big form and a lot of attributes to set, this could lead to very long and unreadable
lines. This is where the **{% set %}** tag can help you. Here is the previous example without
syntax error:

.. code-block:: django

  {% load formica %}

  {% form "formica/base_form.html" %}
    {% set name__size=40 name__class="name" %}
    {% set email__class="email" %}
  {% endform %}

When you use **{% set %}** it add all keyword arguments to the last (and most recent) context. It
works anywhere in your code but it's better to use it in a tag that override current context, like
`{% form %}`_, `{% use %}`_ or even **{% with %}**.

.. _kwargs:

Keyword arguments in tags
=========================

We talk a bit about keyword arguments in these tags. Here is what you should know and what amazing
things you can do.

In all these tags you can pass keyword arguments that would override context for each called block
and tag content. Here are some examples:

.. code-block:: django

  {% load formica %}

  {# Pass wrapper_class to form context #}
  {% form "formica/base_form.html" wrapper_class="horizontal" %}
    {% fields "-email" %}
    {# Change wrapper_class for this field #}
    {% fields "email" wrapper_class="inline horizontal" %}
  {% endform %}

You can do more. We saw the `{% field %}`_ tag can take arguments to override widget attributes but
what if you want to override a specific field without using the `{% field %}`_ tag? (because you
don't want to break field order or forget one). All you need is a variable named
**{{ <field_name>__<name> }}**. Let see it with an example:

.. code-block:: django

  {% load formica %}

  {# Pass wrapper_class to form context #}
  {% form "formica/base_form.html" wrapper_class="horizontal" %}
    {% fields email__wrapper_class="inline horizontal" email__size=40 %}
  {% endform %}

In this example, all fields are rendered with **{{ wrapper_class }}** as **horizontal** except the
**email** field. We also set its widget **size** attribute.

Actually, each time a `{% field %}`_ tag is called (which is the case in `{% fields %}`_ default
block), it checks if any context variable is available for the current field and add them as current
keyword arguments in the tag.

That said, you should keep in mind that if you want this variable interpolation to work, you need
to use `{% field %}`_ tag (within any block you need at that moment).


Template inheritance
====================

Template inheritance within your Formica blocks works the same way as in Django.

You can create your own template and inherit from a base template:

.. code-block:: django

  {% extends "formica/base_form.html" %}

  {# Make a full form #}
  {% block form %}
  <form method="post">
  {{ block.super }}
  <p><input type="submit" value="save" /></p>
  </form>
  {% endblock form %}

If you call `{% form %}`_ with this new template, it will call this block and inherit from the
previous one.
