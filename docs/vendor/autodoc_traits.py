"""autodoc extension for traits

Copyright (c) 2013, Jason Grout
All rights reserved.

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice, this
  list of conditions and the following disclaimer in the documentation and/or
  other materials provided with the distribution.

* Neither the name of the PyThreeJS development team nor the names of its
  contributors may be used to endorse or promote products derived from
  this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

from collections import OrderedDict

from traitlets import TraitType, Undefined, Container, Dict, Any, HasTraits
from sphinx.ext.autodoc import ClassDocumenter, AttributeDocumenter


def dict_info(trait):
    try:
        trait_base = trait._value_trait
    except AttributeError:
        trait_base = trait._trait
    try:
        traits = trait._per_key_traits
    except AttributeError:
        traits = trait._traits

    if traits is None and (trait_base is None or isinstance(trait_base, Any)):
        value_string = 'elements of any type'
    else:
        parts = []
        if traits:
            parts.append('the following types: %r' % {k: v.info() for k,v in traits})
        if trait_base:
            parts.append('values that are: %s' % trait_base.info())
        value_string = 'elements with ' + ', and '.join(parts)

    return '{} with {}'.format(trait.info(), value_string)


def extended_trait_info(trait):
    if isinstance(trait, Dict):
        return dict_info(trait)
    elif isinstance(trait, Container):
        if trait._trait is None:
            return '{} of any type'.format(trait.info())
        return '{} with values that are: {}'.format(trait.info(), trait._trait.info())
    return trait.info()


class HasTraitsDocumenter(ClassDocumenter):
    """Specialized Documenter subclass for traits"""
    objtype = 'hastraits'
    directivetype = 'class'

    @classmethod
    def can_document_member(cls, member, membername, isattr, parent):
        return isinstance(member, HasTraits)

    def get_object_members(self, want_all):
        """Add traits to members list"""
        check, members = super().get_object_members(want_all)
        get_traits = self.object.class_own_traits if self.options.inherited_members \
                     else self.object.class_traits
        members_new = OrderedDict()
        for m in members:
            members_new[m[0]] = m[1]
        traits = tuple(get_traits().items())
        for name, trait in traits:
            if name not in members_new:
                # Don't add a member that would normally be filtered
                continue
                # pass # FIXME: Debugging

            # put help in __doc__ where autodoc will look for it
            trait.__doc__ = trait.help or extended_trait_info(getattr(self.object, name))
            members_new[name] = trait

        return check, [kv for kv in members_new.items()]


class TraitDocumenter(AttributeDocumenter):
    objtype = 'trait'
    directivetype = 'attribute'
    member_order = 1
    priority = 100

    @classmethod
    def can_document_member(cls, member, membername, isattr, parent):
        return isinstance(member, TraitType)

    def format_name(self):
        return self.objpath[-1]

    def add_directive_header(self, sig):
        default = self.object.default_value
        if default is Undefined:
            default_s = ''
        else:
            default_s = repr(default)
        sig = ' = {}({})'.format(
            self.object.__class__.__name__,
            default_s,
        )
        return super().add_directive_header(sig)


def setup(app):
    app.add_autodocumenter(HasTraitsDocumenter)
    app.add_autodocumenter(TraitDocumenter)
