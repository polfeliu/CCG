from typing import TYPE_CHECKING, List, Optional

from .Ctypes import CGenericType, CItemDefinable
from ..style import default_style

if TYPE_CHECKING:
    from ..style import Style
    from ..Cvariable import CVariable
    from ..Cnamespace import CSpace
    from ..doc import Doc


class CStructDefMember:
    """Member of struct definition"""

    def __init__(self,
                 variable: 'CVariable',
                 bitfield: Optional[int] = None,
                 doc: Optional['Doc'] = None
                 ):
        self.variable = variable
        if doc is not None:
            self.variable.doc = doc
        self.bitfield = bitfield
        if bitfield is not None:
            if bitfield > self.variable.bit_size:
                raise ValueError("Bitfields should not be bigger than type size")

    def declaration(self, style: 'Style' = default_style) -> str:
        """Member declaration"""
        return (
            f"{self.variable.declaration(semicolon=False, style=style)}{f': {self.bitfield}' if self.bitfield else ''};"
        )

    @property
    def bit_size(self) -> int:
        if self.bitfield is not None:
            return self.bitfield
        else:
            if self.variable.bit_size is None:
                raise ValueError("Cannot determine bit_size")
            return self.variable.bit_size


class CStruct(CGenericType, CItemDefinable):
    """Struct without inplace definition.

    Assumes struct already is declared"""

    def __init__(self, struct_def: 'CStructDef'):
        super(CStruct, self).__init__(
            name=struct_def.name,
        )
        self.struct_def = struct_def

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
        # Name of the struct type is not checked by hungarian
        pass


class CStructDef(CGenericType, CItemDefinable):
    """Struct with inplace definition"""

    Member = CStructDefMember

    def __init__(self,
                 name: Optional[str] = None,
                 is_packed: bool = False,
                 members: Optional[List[CStructDefMember]] = None,
                 doc: Optional['Doc'] = None
                 ):
        if name is None:
            self.struct_name = ''
            self.is_anonymous = True
        else:
            self.struct_name = name
            self.is_anonymous = False

        super(CStructDef, self).__init__(
            name=f"struct {self.struct_name}",
            doc=doc
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
        """Same struct without inplace definition"""
        return self._struct

    def definition(self,
                   style: 'Style' = default_style,
                   from_space: 'CSpace' = None,
                   doc: bool = False
                   ) -> str:
        self.style_checks(style)

        members = ""
        for member in self.members:
            member_declaration = member.declaration(style=style)
            if style.union_new_line_members:
                member_declaration = style.indent(member_declaration, style.struct_indent_members)
            members += member_declaration
            if member != self.members[-1]:  # Is not last member
                members += str(style.new_line(style.struct_new_line_members))
                members += str(style.space(style.struct_space_members))

        return (
            f"{self.doc_render(style) if doc else ''}"
            f"{self.space_def(from_space)}"
            f"{self.name}"
            f"{style.attribute_packed if self.is_packed else ''}"
            f"{style.open_bracket(style.struct_bracket)}"
            f"{members}"
            f"{style.close_bracket(style.struct_bracket)}"
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
    def bit_size(self, value) -> None:
        # Parent CGenericType will try to set bit_size. Ignore it
        pass
