======
Extras
======

Template filters
================

Formica provides template filters mostly borrowed from
`django-crispy-forms <https://github.com/maraujop/django-crispy-forms>`_.

\|is_input
**********

Returns **True** if field's widget is a ``<input>`` tag, except checkboxe or radio.

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
