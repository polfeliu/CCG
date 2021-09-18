from typing import List
from .Ctypes import *
from .style import default_style

from .Cvariable import CVariable


class CUnion(CGenericType):

    def __init__(self, union_def: 'CUnionDef'):
        super(CUnion, self).__init__(
            name=union_def.name
        )
        self.union_def = union_def

    def definition(self, style: 'Style' = default_style) -> str:
        self.style_checks(style)

        return f"{self.name}"

    def style_checks(self, style: 'Style') -> None:
        # Name of the union type is not checked by hungarian
        pass


class CUnionDef(CGenericType):

    def __init__(self, name: Union[str, None] = None, members: List[CVariable] = None):
        if name is None:
            self.name = ''
            self.is_anonymous = True
        else:
            self.name = name
            self.is_anonymous = False

        super(CUnionDef, self).__init__(
            name=f"union {self.name}"
        )

        if members is None or len(members) < 1:
            raise KeyError("Unions have to have at least one member")

        self.members = members

        self._union = CUnion(
            union_def=self
        )

    def style_checks(self, style: 'Style') -> None:
        # Name of the union type is not checked by hungarian
        pass

    @property
    def union(self) -> CUnion:
        return self._union

    def definition(self, style: 'Style' = default_style) -> str:
        self.style_checks(style)

        members = ""
        for member in self.members:
            member_declaration = member.declaration(style=style)
            if style.new_line_union_members:
                member_declaration = style.indent(member_declaration)
            members += member_declaration
            if member != self.members[-1]:  # Is not last member
                members += style.vnew_line_union_members
                members += style.vspace_union_members
        return (
            f"{self.name}"
            f"{style.bracket_open('union')}"
            f"{members}"
            f"{style.bracket_close('union')}"
        )

    def declaration(self, semicolon: bool = False, style: 'Style' = default_style, from_space: 'CSpace' = None) -> str:
        return self.definition(style) + (';' if semicolon else '')
