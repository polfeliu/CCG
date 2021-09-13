from typing import List
from textwrap import indent
from .types import *


class Union(BasicType):

    def __init__(self, typename: str, members):
        self.type_name = typename
        self.members = members

    def declaration(self, name=None, semicolon=True):
        members = ""
        for member in self.members:
            members += indent(member.declaration(), '\t') + "\n"
        return (
            f"union {self.type_name}{{\n"
            f"{members}"
            f"}}"
        )

    def typedef(self, name, inplace_declaration=True):
        return (
            f"typedef {self.declaration(name=name, semicolon=False) if inplace_declaration else self.type_name + ' ' + name};"
        )
