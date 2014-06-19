# -*- coding: utf-8 -*-
from __future__ import (print_function, division, absolute_import, unicode_literals)

from django import forms
from django.forms.formsets import formset_factory
from django.shortcuts import render


REPEAT_CHOICES = (
    (1, 'days'),
    (2, 'week'),
    (3, 'month'),
)


class RepeatWidget(forms.MultiWidget):
    html = (
        '<label>%(check)s every</label> %(freq)s %(units)s <label>,'
        + ' starting on</label> %(term)s'
    )

    def __init__(self, *args, **kwargs):
        widgets = (
            forms.CheckboxInput(),
            forms.TextInput(attrs={'maxlength': 4, 'size': 1}),
            forms.Select(choices=REPEAT_CHOICES),
            forms.DateInput(attrs={'size': 12}),
        )
        super(RepeatWidget, self).__init__(widgets, *args, **kwargs)

    def format_output(self, rendered_widgets):
        return self.html % {
            'check': rendered_widgets[0],
            'freq': rendered_widgets[1],
            'units': rendered_widgets[2],
            'term': rendered_widgets[3]
        }

    def decompress(self, value):
        return value


class RepeatField(forms.MultiValueField):
    widget = RepeatWidget()

    def __init__(self, *args, **kwargs):
        fields = (
            forms.BooleanField(required=False),
            forms.IntegerField(required=False),
            forms.ChoiceField(required=False, choices=REPEAT_CHOICES),
            forms.DateField(required=False)
        )
        super(RepeatField, self).__init__(fields, *args, **kwargs)

    def compress(self, data_list):
        return {
            'repeat': data_list[0],
            'freq': data_list[1],
            'unit': data_list[2],
            'term': data_list[3]
        }


class CompleteForm(forms.Form):
    CHOICES = (
        (1, 'Cats'),
        (2, 'Dogs'),
        (3, 'Ravens'),
    )

    firstname = forms.CharField(help_text='Sue your parents!', required=False)
    name = forms.CharField()
    yesno = forms.BooleanField(label='Agree?', required=False)

    email = forms.EmailField(help_text="We'd love to spam you forever!")
    url = forms.URLField(help_text='Ze internets!!!')

    number = forms.IntegerField()
    floated = forms.FloatField(label='Float number')

    path = forms.FileField(label='File')
    image = forms.ImageField()
    choices = forms.ChoiceField(
        choices=CHOICES, initial=3,
        help_text='We already selected the smartest for you.'
    )
    sure = forms.BooleanField(
        label='You sure?', required=True,
        help_text='Should you have the choice'
    )
    text = forms.CharField(required=False, widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}))
    mchoices = forms.MultipleChoiceField(label='Multiple choices', choices=CHOICES)
    choices2 = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    mchoices2 = forms.MultipleChoiceField(
        label='Multiple choices', choices=CHOICES,
        widget=forms.CheckboxSelectMultiple
    )
    maybe = forms.NullBooleanField(required=False)
    ip = forms.IPAddressField(label='IP Address')
    decimal = forms.DecimalField()
    repeat = RepeatField(
        label='Repeat', initial=(False, None, None, None),
        help_text='Complext widget', required=False
    )

    date = forms.DateField()
    time = forms.TimeField()

    datetime = forms.DateTimeField(label='Date and time')
    splitdatetime = forms.SplitDateTimeField(label='Date and Time')

    # Convenient way to have some field groups.
    # You don't need to do it and can use field names in your templates but in this
    # case it was easier to use such a trick :)
    field_groups = (
        ('firstname', 'name', 'yesno'),
        ('email', 'url'),
        ('number', 'floated'),
        (
            'path', 'image', 'choices', 'sure', 'text',
            'mchoices', 'choices2', 'mchoices2', 'maybe', 'ip', 'decimal',
            'repeat'
        ),
        ('date', 'time'),
        ('datetime', 'splitdatetime',)
    )


class TableForm(forms.Form):
    qty = forms.IntegerField(label='Qty.')
    name = forms.CharField(label='Name', max_length=40)
    date = forms.DateField(label='Date', required=False)
    mch = forms.ChoiceField(
        label='Pick one',
        choices=((1, 'Dogs'), (2, 'Cats'), (3, 'Birds')),
        widget=forms.Select,
    )


SimpleFormset = formset_factory(TableForm, extra=4, can_delete=True, can_order=False)


def home(request):
    return render(request, 'home.html')


def form_view(request, template_name):
    form = CompleteForm(request.POST or None)
    form.is_valid()

    formset = SimpleFormset(request.POST or None)
    formset.is_valid()

    return render(request, template_name, {
        'form': form,
        'formset': formset,
    })
