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
        if bitfield is not None:
            if bitfield > self.variable.c_type.bit_size:
                raise ValueError("Bitfields should not be bigger than type size")

    def declaration(self, style: 'Style' = default_style) -> str:
        return (
            f"{self.variable.declaration(semicolon=False, style=style)}{f': {self.bitfield}' if self.bitfield else ''};"
        )

    @property
    def bit_size(self) -> int:
        if self.bitfield is not None:
            return self.bitfield
        else:
            return self.variable.bit_size


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
                 is_packed: bool = False,
                 members: Union[List[CStructDefMember], None] = None):
        if name is None:
            self.struct_name = ''
            self.is_anonymous = True
        else:
            self.struct_name = name
            self.is_anonymous = False

        super(CStructDef, self).__init__(
            name=f"struct {self.struct_name}"
        )

        if members is None or len(members) < 1:
            raise KeyError("Structs have to have at least one struct member")

        self.is_packed = is_packed
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
            f"{style.attribute_packed if self.is_packed else ''}"
            f"{style.bracket_open('struct')}"
            f"{members}"
            f"{style.bracket_close('struct')}"
        )

    def declaration(self, semicolon: bool = False, style: 'Style' = default_style, from_space: 'CSpace' = None) -> str:
        return self.definition(style) + (';' if semicolon else '')

    @property
    def bit_size(self) -> int:
        if not self.is_packed:
            raise MemoryError(
                "Cannot compute the bit_size of a non-packed struct"
            )
        else:
            return sum(
                [member.bit_size for member in self.members]
            )

    @bit_size.setter
    def bit_size(self, value):
        # Parent CGenericType will try to set bit_size. Ignore it
        pass
