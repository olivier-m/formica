# -*- coding: utf-8 -*-
#
# This file is part of Formica released under the FreeBSD license.
# See the LICENSE for more information.
from __future__ import (print_function, division, absolute_import, unicode_literals)

from contextlib import contextmanager
import re

from django import forms
from django.template.base import parse_bits
from django.template.loader import get_template
from django.template.loader_tags import BlockNode, BlockContext, ExtendsNode, BLOCK_CONTEXT_KEY
from django import template
from django.utils import six


register = template.Library()

RE_ATTR = re.compile(r'^([a-z]+|data_.+)$')


def get_widget_attrs(attrs):
    """
    Returns only attributes in whole word or starting with data_
    """
    return dict([
        (k.replace('_', '-').lower(), v)
        for k, v in attrs.items()
        if RE_ATTR.match(k) and v is not None
    ])


def get_field_context(field, context):
    """
    Search for <fieldname>__<varname> patterns in context
    """
    s = '{0}__'.format(field.name)
    _ctx = {}
    attrs = {}
    ctx = {}
    for data in context.dicts:
        _ctx.update(dict((k[len(s):], v) for k, v in data.items() if k.startswith(s)))

    # Dispatch attribute values from context values
    for k, v in _ctx.items():
        if RE_ATTR.match(k):
            if v is not None:
                attrs[k] = v
        else:
            ctx[k] = v

    return ctx, attrs


@contextmanager
def extra_context(context, *args, **kwargs):
    with_render_context = len(args) > 0

    if with_render_context:
        context.render_context.dicts.append({BLOCK_CONTEXT_KEY: args[0]})
    context.update(kwargs)
    yield

    context.pop()
    if with_render_context:
        context.render_context.pop()


def use_template(klass):
    def wrapper(parser, token):
        bits = token.split_contents()

        tag_name = bits.pop(0)
        if len(bits) == 0:
            raise template.TemplateSyntaxError(
                '"{0}" tag takes at least 1 argument: the template name'.format(tag_name)
            )

        args, kwargs = parse_bits(parser, bits, ['template_name'], '', '', None, False, 'form')

        nodelist = parser.parse(('end{0}'.format(tag_name),))
        template_name = args.pop(0)
        parser.delete_first_token()

        return klass(nodelist, tag_name, template_name, *args, **kwargs)

    return wrapper


class UseTemplateNode(template.Node):
    CONTENTS_CONTEXT_KEY = 'contents'

    def __init__(self, nodelist, tag_name, template_name, *args, **kwargs):
        self.nodelist = nodelist
        self.tag_name = tag_name
        self.template_name = template_name
        self.args = args
        self.kwargs = kwargs

    def resolve_blocks(self, context, template, blocks=None):
        """
        Get all the blocks from this template, accounting for 'extends' tags
        """
        if blocks is None:
            blocks = BlockContext()

        # If it's just the name, resolve into template
        if isinstance(template, six.string_types):
            template = get_template(template)

        # Add this templates blocks as the first
        local_blocks = dict(
            (block.name, block)
            for block in template.nodelist.get_nodes_by_type(BlockNode)
        )
        blocks.add_blocks(local_blocks)

        # Do we extend a parent template?
        extends = template.nodelist.get_nodes_by_type(ExtendsNode)
        if extends:
            # Can only have one extends in a template
            extends_node = extends[0]

            # Get the parent, and recurse
            parent_template = extends_node.get_parent(context)
            self.resolve_blocks(context, parent_template, blocks)

        return blocks

    def get_context(self, context):
        return dict((k, v.resolve(context)) for k, v in self.kwargs.items())

    def get_block_name(self, context):
        if len(self.args) == 0:
            raise template.TemplateSyntaxError(
                'No block name provided in "{0}" tag.'.format(self.tag_name)
            )
        block_name = self.args[0].resolve(context)
        if block_name in (None, ''):
            raise ValueError('No block name in tag "{0}"'.format(self.tag_name))

        return block_name

    def render(self, context):
        template_name = self.template_name.resolve(context)
        if not template_name:
            raise template.TemplateSyntaxError(
                'Invalid template name in "{0}"'.format(self.tag_name))

        # Get block_name
        block_name = self.get_block_name(context)

        # Set context dict based on kwargs
        ctx = self.get_context(context)

        # Loading blocks from template
        blocks = self.resolve_blocks(context, template_name)

        # First render node contents using our new blocks and context
        with extra_context(context, blocks, **ctx):
            ctx[self.CONTENTS_CONTEXT_KEY] = self.nodelist.render(context)

        # Then, render form node, using its contents
        with extra_context(context, blocks, **ctx):
            return blocks.get_block(block_name).render(context)


class FormTemplateNode(UseTemplateNode):
    INSTANCE_CONTEXT_KEY = 'form'

    def __init__(self, nodelist, tag_name, template_name, form=None, **kwargs):
        super(FormTemplateNode, self).__init__(nodelist, tag_name, template_name, **kwargs)
        self.form = form

    def get_block_name(self, context):
        return 'form'

    def get_context(self, context):
        ctx = super(FormTemplateNode, self).get_context(context)
        form = self.form
        if form is not None:
            form = form.resolve(context)
        else:
            form = context.get('form')

        if form is None:
            raise template.TemplateSyntaxError('No form to render in form tag.')

        ctx[self.INSTANCE_CONTEXT_KEY] = form
        ctx['with_csrf'] = ctx.get('with_csrf', True)

        return ctx


#
# Tags
#
register.tag('use', use_template(UseTemplateNode))
register.tag('form', use_template(FormTemplateNode))


@register.simple_tag(takes_context=True)
def field(context, field, block_name='field', **kwargs):
    if FormTemplateNode.INSTANCE_CONTEXT_KEY not in context:
        raise ValueError('"field" tag should be in a "form" tag with a valid form.')

    form = context[FormTemplateNode.INSTANCE_CONTEXT_KEY]
    blocks = context.render_context[BLOCK_CONTEXT_KEY]
    block = blocks.get_block(block_name)
    if block is None:
        raise ValueError('Block "{0}" does not exist.'.format(block_name))

    if isinstance(field, six.string_types):
        if field not in form.fields:
            raise ValueError('Field "{0}" does not exist'.format(field))
        field = form[field]

    # Set new context and widget attributes based on kwargs and current context
    ctx, attrs = get_field_context(field, context)
    ctx.update(kwargs)
    ctx['attrs'] = attrs

    attrs.update(get_widget_attrs(kwargs))
    field.field.widget.attrs.update(attrs)

    ctx['field'] = field

    with extra_context(context, blocks, **ctx):
        return block.render(context)


@register.simple_tag(takes_context=True)
def fields(context, field_list='', block_name='fields', **kwargs):
    if FormTemplateNode.INSTANCE_CONTEXT_KEY not in context:
        raise ValueError('"fields" tag should be in a "form" tag.')

    form = context[FormTemplateNode.INSTANCE_CONTEXT_KEY]
    blocks = context.render_context[BLOCK_CONTEXT_KEY]
    block = blocks.get_block(block_name)
    if block is None:
        raise ValueError('Block "{0}" does not exist.'.format(block_name))

    # Make field list
    if isinstance(field_list, (list, tuple)):
        # List could be a list of strings or field instances...
        _list = [isinstance(x, six.string_types) and x or x.name for x in field_list]
    else:
        # ... or a space separated list of names
        field_list = field_list.strip()
        _list = field_list and re.split(r'[ ,]+', field_list) or []

    excluded_fields = [x[1:] for x in _list if x.startswith('-')]
    fields = [x for x in _list if not x.startswith('-')]
    if len(fields) == 0:
        fields = [x.name for x in form]

    kwargs['fields'] = [form[x] for x in fields if x not in excluded_fields]

    with extra_context(context, blocks, **kwargs):
        return block.render(context)


@register.simple_tag(takes_context=True)
def useblock(context, block_name, **kwargs):
    blocks = context.render_context[BLOCK_CONTEXT_KEY]
    block = blocks.get_block(block_name)
    if block is None:
        raise ValueError('Block "{0}" does not exist.'.format(block_name))

    with extra_context(context, blocks, **kwargs):
        return block.render(context)


@register.simple_tag(name='set', takes_context=True)
def _set(context, **kwargs):
    last_context = context.dicts[-1:]
    if len(last_context) > 0:
        last_context[0].update(**kwargs)

    return ''


#
# Filters
#
@register.filter
def is_input(field):
    return (isinstance(field.field.widget, forms.widgets.Input) and
            not isinstance(field.field.widget, forms.FileInput))


@register.filter
def is_textarea(field):
    return isinstance(field.field.widget, forms.Textarea)


@register.filter
def is_select(field):
    return (isinstance(field.field.widget, forms.Select) and
            not isinstance(field.field.widget, forms.widgets.RendererMixin))


@register.filter
def is_checkbox(field):
    return isinstance(field.field.widget, forms.CheckboxInput)


@register.filter
def is_password(field):
    return isinstance(field.field.widget, forms.PasswordInput)


@register.filter
def is_radioselect(field):
    return isinstance(field.field.widget, forms.RadioSelect)


@register.filter
def is_checkboxselectmultiple(field):
    return isinstance(field.field.widget, forms.CheckboxSelectMultiple)


@register.filter
def is_file(field):
    return isinstance(field.field.widget, forms.FileInput)


@register.filter
def any_field_error(fields):
    fields = fields if isinstance(fields, (list, tuple)) else [fields]
    return any(len(x.errors) > 0 for x in fields)


@register.filter
def any_field_required(fields):
    fields = fields if isinstance(fields, (list, tuple)) else [fields]
    return any(x.field.required for x in fields)
