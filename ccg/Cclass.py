from typing import TYPE_CHECKING, List, Union
from enum import Enum

from .style import Style, default_style
from .types import CGenericType

from .variable import CVariable
from .function import CFunction

if TYPE_CHECKING:
    from .function import CFunctionArgument


class CClassAccess(Enum):
    public = 0
    protected = 1
    private = 2


class CClassAttribute(CVariable):

    def __init__(self, variable: 'CVariable', access: CClassAccess = CClassAccess.private):
        self.variable = variable
        self.access = access

    def declaration(self, style: 'Style' = default_style) -> str:
        return (
            f"{self.variable.declaration(semicolon=False, style=style)}{f': {self.bitfield}' if self.bitfield else ''};"
        )


class CClassMethod(CFunction):

    def __init__(self,
                 name: str,
                 return_type: Union[CGenericType, None] = None,
                 arguments: Union[List['CFunctionArgument'], None] = None,
                 content=None,
                 access: CClassAccess = CClassAccess.private
                 ):
        super(CClassMethod, self).__init__(
            name=name,
            return_type=return_type,
            arguments=arguments,
            content=content
        )
        self.access = access


class CClassConstructor(CClassMethod):

    def __init__(self,
                 arguments: Union[List['CFunctionArgument'], None] = None,  # TODO Static initialization of attributes
                 content=None,
                 access: CClassAccess = CClassAccess.private
                 ):
        super(CClassMethod, self).__init__(
            name='',  # Name of the function is injected by Cclass TODO
            return_type=None,  # Ensure no type is placed here
            arguments=arguments,
            content=content
        )
        self.access = access


class CClass(CGenericType):

    def __init__(self,
                 name: str,
                 members: List[Union[CClassConstructor, CClassAttribute, CClassMethod]]
                 ):
        super(CClass, self).__init__(
            name=name,
        )
        self.members = members

    def declaration(self, semicolon: bool = True, style: 'Style' = default_style) -> str:
        self.style_checks(style)
        # TODO This does not match inheriting functionality. The base class will be refactor as naming is wrong
        return f"class {self.name}{';' if semicolon else ''}"

    def _member_definition(self, style: 'Style') -> str:
        members = ""
        if style.class_members == Style.ClassMembers.inline_access_preserve_order:
            for member in self.members:
                members += style.indent(
                    f"{member.access.name} "
                    #f"{member.declaration()}", TODO
                    "class_member"
                )
        return members

    def definition(self, style: 'Style' = default_style) -> str:
        self.style_checks(style)

        return (
            f"{self.declaration(False, style)}"
            f"{style.bracket_open('class')}"
            f"{self._member_definition(style)}"
            f"{style.bracket_close('class')}"
        )

    def all_methods_definition(self):
        raise NotImplemented

    def style_checks(self, style: 'Style') -> None:
        pass  # TODO
