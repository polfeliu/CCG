from typing import List
from textwrap import indent
from .types import *

from .style import default_style

class StructMember:

    def __init__(self, variable, bitfield=None):
        self.variable = variable
        self.bitfield = bitfield

    def declaration(self, style: 'Style' = default_style):
        return (
            f"{self.variable.declaration(semicolon=False, style=style)}{f': {self.bitfield}' if self.bitfield else ''};"
        )


class CStruct(CBasicType):

    def __init__(self, type_name: str, members: List[StructMember]):
        super(CStruct, self).__init__(
            type_name=type_name
        )
        self.members = members

    members: List[StructMember] = []

    def declaration(self, name=None, semicolon=True, style: 'Style' = default_style):
        if style is not None:
            if style.check_hungarian:
                self.check_hungarian()

        members = ""
        for member in self.members:
            members += indent(member.declaration(style=style), '\t') + "\n"
        return (
            f"struct {self.type_name}{{\n"
            f"{members}"
            f"}}"
        )

    def typedef(self, name, inplace_declaration=True, style: 'Style' = default_style):
        return (
            f"typedef {self.declaration(name=name, semicolon=False, style=style) if inplace_declaration else self.type_name + ' ' + name};"
        )
