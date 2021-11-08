from typing import TYPE_CHECKING, List, Optional
from .Ctypes import CGenericType, CItemDefinable
from ..Cvariable import CVariable
from ..style import default_style

if TYPE_CHECKING:
    from ..style import Style
    from ..Cnamespace import CSpace
    from ..doc import Doc


class CUnion(CGenericType, CItemDefinable):

    def __init__(self, union_def: 'CUnionDef'):
        super(CUnion, self).__init__(
            name=union_def.name
        )
        self.union_def = union_def

    def definition(self,
                   style: 'Style' = default_style,
                   from_space: 'CSpace' = None,
                   doc: bool = False
                   ) -> str:
        self.style_checks(style)

        return (
            f"{self.space_def(from_space)}"
            f"{self.name}"
        )

    def style_checks(self, style: 'Style') -> None:
        # Name of the union type is not checked by hungarian
        pass


class CUnionDef(CGenericType, CItemDefinable):

    def __init__(self,
                 name: Optional[str] = None,
                 members: List[CVariable] = None,
                 doc: Optional['Doc'] = None
                 ):
        if name is None:
            self.name = ''
            self.is_anonymous = True
        else:
            self.name = name
            self.is_anonymous = False

        super(CUnionDef, self).__init__(
            name=f"union {self.name}",
            doc=doc
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

    def definition(self,
                   style: 'Style' = default_style,
                   from_space: 'CSpace' = None,
                   doc: bool = False
                   ) -> str:
        self.style_checks(style)

        members = ""
        for member in self.members:
            member_declaration = member.declaration(style=style)
            if style.new_line_union_members:
                member_declaration = style.indent(member_declaration)
            members += member_declaration
            if member != self.members[-1]:  # Is not last member
                members += str(style.new_line(style.new_line_union_members))
                members += str(style.space(style.space_union_members))
        return (
            f"{self.doc_render(style) if doc else ''}"
            f"{self.space_def(from_space)}"
            f"{self.name}"
            f"{style.open_bracket(style.union_bracket)}"
            f"{members}"
            f"{style.close_bracket(style.union_bracket)}"
        )

    def declaration(self,
                    style: 'Style' = default_style,
                    semicolon: bool = True,
                    doc: bool = True,
                    from_space: 'CSpace' = None,
                    without_arguments: bool = False,
                    for_variable: bool = False
                    ) -> str:
        return self.definition(style=style, from_space=from_space, doc=doc) + (';' if semicolon else '')
