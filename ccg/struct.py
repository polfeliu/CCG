from typing import List
from textwrap import indent
from .types import *


class StructMember():

    def __init__(self, variable, bitfield=None):
        self.variable = variable
        self.bitfield = bitfield

    def declaration(self):
        return (
            f"{self.variable.declaration(semicolon=False)}{f': {self.bitfield}' if self.bitfield else ''};"
        )


class Struct(BasicType):

    def __init__(self, type_name: str, members: List[StructMember]):
        self.type_name = type_name
        self.members = members

    members: List[StructMember] = []

    # TODO Hungarian notation

    def declaration(self, name=None, semicolon=True):
        members = ""
        for member in self.members:
            members += indent(member.declaration(), '\t') + "\n"
        return (
            f"struct {self.type_name}{{\n"
            f"{members}"
            f"}}"
        )

    def typedef(self, name, inplace_declaration=True):
        return (
            f"typedef {self.declaration(name=name, semicolon=False) if inplace_declaration else self.type_name + ' ' + name};"
        )
