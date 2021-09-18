from typing import List
from textwrap import indent
from .types import *

from .style import default_style


class CStructMember:

    def __init__(self, variable, bitfield=None):
        self.variable = variable
        self.bitfield = bitfield

    def declaration(self, style: 'Style' = default_style):
        return (
            f"{self.variable.declaration(semicolon=False, style=style)}{f': {self.bitfield}' if self.bitfield else ''};"
        )


class CStruct(CBasicType):

    def __init__(self, struct_def: 'CStructDef'):
        super(CStruct, self).__init__(
            type_name=struct_def.type_name
        )
        self.struct_def = struct_def

    def definition(self, style: 'Style' = default_style) -> str:
        self.style_checks(style)

        return f"{self.type_name}"

    def style_checks(self, style: 'Style'):
        # Name of the struct type is not checked by hungarian
        pass


class CStructDef(CBasicType):

    def __init__(self, name: Union[str, None] = None, members: List[CStructMember] = None):
        if name is None:
            self.name = ''
            self.is_anonymous = True
        else:
            self.name = name
            self.is_anonymous = False

        super(CStructDef, self).__init__(
            type_name=f"struct {self.name}"
        )

        if members is None or len(members) < 1:
            raise KeyError("Structs have to have at least one struct member")

        self.members = members

        self._struct = CStruct(
            struct_def=self
        )

    def style_checks(self, style: 'Style'):
        # Name of the struct type is not checked by hungarian
        pass

    @property
    def struct(self):
        return self._struct

    def definition(self, style: 'Style' = default_style) -> str:
        self.style_checks(style)

        members = ""
        for member in self.members:
            member_declaration = member.declaration(style=style)
            if style.new_line_union_members:
                member_declaration = style.indent(member_declaration)
            members += member_declaration
            if member != self.members[-1]:  # Is not last member
                members += style.vnew_line_struct_members
                members += style.vspace_struct_members
        return (
            f"{self.type_name}"
            f"{style.bracket_open('struct')}"
            f"{members}"
            f"{style.bracket_close('struct')}"
        )

    def declaration(self, semicolon: bool = False, style: 'Style' = default_style):
        return self.definition(style) + (';' if semicolon else '')
