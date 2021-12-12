from enum import Enum
from typing import TYPE_CHECKING, List, Optional

from .Ctypes import CGenericItem
from ..style import default_style

if TYPE_CHECKING:
    from .CstdTypes import CIntegerType
    from ..doc import Doc
    from ..Cnamespace import CSpace
    from ..style import Style
    from ..expressions.Cexpression import CExpression


class CEnumMember:

    def __init__(self,
                 name: str,
                 value: Optional['CExpression'] = None
                 ):
        self.name = name
        self.value = value

    def render(self, style: 'Style' = default_style):
        if self.value is None:
            return self.name
        else:
            return f"{self.name} = {self.value.render(style=style)}"


class CEnum(CGenericItem):
    Member = CEnumMember

    class Key(Enum):
        enum = 'enum'
        enum_class = 'enum class'
        enum_struct = 'enum struct'

    def __init__(self,
                 members: List[CEnumMember] = None,
                 name: str = None,
                 key: Key = Key.enum,
                 base_type: 'CIntegerType' = None,
                 in_space: Optional['CSpace'] = None,
                 doc: Optional['Doc'] = None
                 ):
        super(CEnum, self).__init__(
            name=name,
            in_space=in_space,
            doc=doc
        )
        if members is None:
            self.members = []
        else:
            self.members = members

        self.key = key
        self.base_type = base_type

    def declaration(self,
                    style: 'Style' = default_style,
                    semicolon: bool = True,
                    doc: bool = True,
                    from_space: 'CSpace' = None
                    ) -> str:
        members = style.token_separated_members(
            token=",",
            members=[member.render(style) for member in self.members],
            new_line=style.enum_new_line_members,
            indent=style.enum_indent_members,
            space=style.enum_space_members
        )
        return (
            f"{self.key.value}"
            f"{self.name if self.name is not None else ''}"
            f"{self.base_type.declaration(style=style, semicolon=False, from_space=from_space, for_variable=True) if self.base_type is not None else ''}"
            f"{style.open_bracket(style.enum_bracket)}"
            f"{members}"
            f"{style.close_bracket(style.enum_bracket)}"
            f";"  # TODO ??
        )
