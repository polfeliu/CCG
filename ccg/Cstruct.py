from typing import TYPE_CHECKING, List, Union

from .style import default_style
from .Ctypes import CGenericType

if TYPE_CHECKING:
    from .style import Style
    from .Cvariable import CVariable
    from .Cnamespace import CSpace


class CStructDefMember:

    def __init__(self, variable: 'CVariable', bitfield: Union[int, None] = None):
        self.variable = variable
        self.bitfield = bitfield

    def declaration(self, style: 'Style' = default_style) -> str:
        return (
            f"{self.variable.declaration(semicolon=False, style=style)}{f': {self.bitfield}' if self.bitfield else ''};"
        )


class CStruct(CGenericType):

    def __init__(self, struct_def: 'CStructDef'):
        super(CStruct, self).__init__(
            name=struct_def.name,
        )
        self.struct_def = struct_def

    def definition(self, style: 'Style' = default_style) -> str:
        self.style_checks(style)

        return f"{self.name}"

    def style_checks(self, style: 'Style') -> None:
        # Name of the struct type is not checked by hungarian
        pass


class CStructDef(CGenericType):
    Member = CStructDefMember

    def __init__(self,
                 name: Union[str, None] = None,
                 members: Union[List[CStructDefMember], None] = None):
        if name is None:
            self.name = ''
            self.is_anonymous = True
        else:
            self.name = name
            self.is_anonymous = False

        super(CStructDef, self).__init__(
            name=f"struct {self.name}"
        )

        if members is None or len(members) < 1:
            raise KeyError("Structs have to have at least one struct member")

        self.members = members

        self._struct = CStruct(
            struct_def=self
        )

    def style_checks(self, style: 'Style') -> None:
        # Name of the struct type is not checked by hungarian
        pass

    @property
    def struct(self) -> CStruct:
        return self._struct

    def definition(self, style: 'Style' = default_style) -> str:
        self.style_checks(style)

        members = ""
        for member in self.members:
            member_declaration = member.declaration(style=style)
            if style.new_line_union_members:
                member_declaration = style.indent(member_declaration, 'struct_member')
            members += member_declaration
            if member != self.members[-1]:  # Is not last member
                members += style.vnew_line_struct_members
                members += style.vspace_struct_members
        return (
            f"{self.name}"
            f"{style.bracket_open('struct')}"
            f"{members}"
            f"{style.bracket_close('struct')}"
        )

    def declaration(self, semicolon: bool = False, style: 'Style' = default_style, from_space: 'CSpace' = None) -> str:
        return self.definition(style) + (';' if semicolon else '')
