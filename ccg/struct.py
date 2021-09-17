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

        return f"struct {self.type_name}"

    def style_checks(self, style: 'Style'):
        # Name of the struct type is not checked by hungarian
        pass


class CStructDef(CBasicType):

    def __init__(self, name: Union[str, None] = None, members: List[CStructMember] = None):
        super(CStructDef, self).__init__(
            type_name=f"struct {name}"
        )

        if members is None or len(members) < 1:
            raise KeyError("Structs have to have at least one struct member")

        self.members = members

        self.name = name
        self._struct = CStruct(
            struct_def=self
        )

    def style_checks(self, style: 'Style'):
        # Name of the struct type is not checked by hungarian
        pass

    @property
    def is_anonymous(self):
        # If struct definition doesn't have a name the struct is anonymous
        return self.name is None

    @property
    def struct(self):
        return self._struct

    def definition(self, style: 'Style' = default_style) -> str:
        self.style_checks(style)
        print(style.vbracket_struct_bracket_open)
        members = ""
        for member in self.members:
            members += indent(member.declaration(style=style), '\t') + "\n"
        return (
            f"{self.type_name}"
            f""  # TODO newline
            f"{members}"
            f"}}"
        )

    def declaration(self, semicolon: bool = False, style: 'Style' = default_style):
        return self.definition(style)
