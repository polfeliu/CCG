from enum import Enum
from typing import TYPE_CHECKING, List, Union, Any

from .Cfunction import CFunction
from .Ctypes import CGenericType, CVoidType, CNoType
from .Cvariable import CVariable
from .style import Style, default_style

if TYPE_CHECKING:
    from .Cfunction import CFunctionArgument
    from .Cnamespace import CSpace


class CClassAccess(Enum):
    public = 0
    protected = 1
    private = 2


# TODO Static methods and attributes
class CClassAttribute(CVariable):

    def __init__(self,
                 name: str,
                 c_type: 'CGenericType',
                 initial_value: Any = None,
                 access: CClassAccess = CClassAccess.private
                 ):
        super(CClassAttribute, self).__init__(
            name=name,
            c_type=c_type,
            initial_value=initial_value
        )
        self.access = access


class CClassMethod(CFunction):

    def __init__(self,
                 name: str,
                 return_type: CGenericType = CVoidType,
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
            return_type=CNoType,  # Ensure no type is placed here
            arguments=arguments,
            content=content
        )
        self.access = access


class CClass(CGenericType):
    Access = CClassAccess
    Attribute = CClassAttribute
    Method = CClassMethod
    Constructor = CClassConstructor

    def __init__(self,
                 name: str,
                 members: List[Union[CClassConstructor, CClassAttribute, CClassMethod]]
                 ):
        super(CClass, self).__init__(
            name=name,
        )
        self.members = members

        for member in self.members:
            if isinstance(member, CClassConstructor):
                member.name = self.name
            member.in_space = self

    def declaration(self, semicolon: bool = True, style: 'Style' = default_style, from_space: 'CSpace' = None) -> str:
        self.style_checks(style)
        return f"class {self.name}{';' if semicolon else ''}"

    def _member_definition(self, style: 'Style') -> str:
        content = ""
        if style.class_members == Style.ClassMembers.inline_access_preserve_order:
            for member in self.members:
                content += style.indent(
                    f"{member.access.name}: "
                    f"{member.declaration(from_space=self)}",
                    "class_member"
                )
        if style.class_members == Style.ClassMembers.group_by_access_specified:
            access_contents = []
            for access in CClassAccess:
                access_members = [member for member in self.members if member.access == access]
                if len(access_members) > 0:
                    access_content = f"{access.name}:\n"

                    for member in access_members:
                        access_content += style.indent(member.declaration(from_space=self), "class_member")

                    access_content = style.indent(access_content, "class_access")
                    access_contents.append(access_content)
            for access_content in access_contents:
                content += access_content + ('\n' if access_content is not access_contents[-1] else '')

        return content

    def definition(self, style: 'Style' = default_style) -> str:
        self.style_checks(style)

        return (
            f"{self.declaration(False, style)}"
            f"{style.bracket_open('class')}"
            f"{self._member_definition(style)}"
            f"{style.bracket_close('class')};"
        )

    def all_members_definition(self) -> List[str]:
        return [
            member.definition()
            for member
            in self.members
            if not isinstance(member, CClassAttribute)
        ]

    def style_checks(self, style: 'Style') -> None:
        pass
