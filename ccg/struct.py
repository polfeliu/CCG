from typing import List
from textwrap import indent
from .types import *


class StructMember:

    def __init__(self, variable, bitfield=None):
        self.variable = variable
        self.bitfield = bitfield

    def declaration(self, style: Union['Style', None] = None):
        return (
            f"{self.variable.declaration(semicolon=False, style=style)}{f': {self.bitfield}' if self.bitfield else ''};"
        )


class CStruct(CBasicType):

    def __init__(self, type_name: str, members: List[StructMember]):
        super(CStruct, self).__init__(
            type_name=type_name,
            hungarian_prefix="t"
        )
        self.members = members

    members: List[StructMember] = []

    # TODO Hungarian notation

    def declaration(self, name=None, semicolon=True, style: Union['Style', None] = None):
        members = ""
        for member in self.members:
            members += indent(member.declaration(style=style), '\t') + "\n"
        return (
            f"struct {self.type_name}{{\n"
            f"{members}"
            f"}}"
        )

    def typedef(self, name, inplace_declaration=True, style: Union['Style', None] = None):
        return (
            f"typedef {self.declaration(name=name, semicolon=False, style=style) if inplace_declaration else self.type_name + ' ' + name};"
        )
