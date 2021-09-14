from typing import List
from textwrap import indent
from .types import *
from .style import default_style

from .variable import CVariable


class CUnion(CBasicType):

    def __init__(self, type_name: str, members: List[CVariable]):
        super(CUnion, self).__init__(
            type_name=type_name,
            hungarian_prefix="u"
        )
        self.type_name = type_name
        self.members = members

    def declaration(self, name=None, semicolon=True, style: 'Style' = default_style):
        members = ""
        for member in self.members:
            members += indent(member.declaration(), '\t') + "\n"
        return (
            f"union {self.type_name}{{\n"
            f"{members}"
            f"}}"
        )

    def typedef(self, name, inplace_declaration=True, style: 'Style' = default_style):
        return (
            f"typedef {self.declaration(name=name, semicolon=False, style=style) if inplace_declaration else self.type_name + ' ' + name};"
        )
