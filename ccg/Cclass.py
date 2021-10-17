from enum import Enum
from typing import TYPE_CHECKING, List, Union, Any
from abc import ABC, abstractmethod

from .Cfunction import CFunction
from .Ctypes import CGenericType, CVoidType, CNoType, CGenericItem
from .Cusing import CUsing
from .Cvariable import CVariable
from .style import Style, default_style

if TYPE_CHECKING:
    from .Cfunction import CFunctionArgument
    from .Cnamespace import CSpace
    from .Ctypes import CGenericItem
    from .doc import Doc


class CClassAccess(Enum):
    public = 0
    protected = 1
    private = 2


class CClassMember(ABC):

    def __init__(self, access: CClassAccess = CClassAccess.private):
        self.access = access

    @abstractmethod
    def declaration(self,
                    style: 'Style' = default_style,
                    semicolon: bool = True,
                    doc: bool = True,
                    from_space: 'CSpace' = None
                    ) -> str:
        """All Class Members should inherit from a CGenericItem that contains a Declaration"""
        raise NotImplemented

    @abstractmethod
    def doc_render(self, style: 'Style') -> str:
        """All Class members should have a doc_render method"""
        raise NotImplemented

    doc = None


class CClassAttribute(CVariable, CClassMember):

    def __init__(self,
                 name: str,
                 c_type: 'CGenericType',
                 initial_value: Any = None,
                 access: CClassAccess = CClassAccess.private,
                 static: bool = False, const: bool = False, constexpr: bool = False,
                 auto_hungarize: bool = False,
                 doc: Union['Doc', None] = None
                 ):
        CVariable.__init__(self,
                           name=name,
                           c_type=c_type,
                           initial_value=initial_value,
                           static=static,
                           const=const,
                           constexpr=constexpr,
                           auto_hungarize=auto_hungarize,
                           doc=doc
                           )

        CClassMember.__init__(self, access)


class CClassMethod(CFunction, CClassMember):

    def __init__(self,
                 name: str,
                 return_type: CGenericType = CVoidType,
                 arguments: Union[List['CFunctionArgument'], None] = None,
                 content=None,
                 access: CClassAccess = CClassAccess.private,
                 static: bool = False,
                 doc: Union['Doc', None] = None
                 ):
        CFunction.__init__(self,
                           name=name,
                           return_type=return_type,
                           arguments=arguments,
                           content=content,
                           static=static,
                           doc=doc
                           )
        CClassMember.__init__(self, access)


class CClassConstructor(CClassMethod):

    def __init__(self,
                 arguments: Union[List['CFunctionArgument'], None] = None,
                 content=None,
                 access: CClassAccess = CClassAccess.private
                 ):
        CClassMethod.__init__(self,
                              name='',  # Name of the function is injected by Cclass
                              return_type=CNoType,  # Ensure no type is placed here
                              arguments=arguments,
                              content=content,
                              access=access
                              )


class ClassTypeMember(CClassMember):
    def __init__(self,
                 member: CGenericType,
                 access: CClassAccess = CClassAccess.private
                 ):
        CClassMember.__init__(self, access)
        self.member = member

    def declaration(self,
                    style: 'Style' = default_style,
                    semicolon: bool = True,
                    doc: bool = True,
                    from_space: 'CSpace' = None
                    ) -> str:
        return self.member.typedef(style=style, from_space=from_space)

    def doc_render(self, style: 'Style') -> str:
        return ""  # TODO


class CClassUsing(CUsing, CClassMember):

    def __init__(self,
                 item: 'CGenericItem',
                 access: CClassAccess = CClassAccess.private
                 ):
        CUsing.__init__(self, item)
        CClassMember.__init__(self, access)


class CClassInheritance:

    def __init__(self, cls: 'CClass', access: CClassAccess = CClassAccess.private):
        self.cls = cls
        self.access = access


class CClass(CGenericType):
    Access = CClassAccess
    Attribute = CClassAttribute
    Method = CClassMethod
    Constructor = CClassConstructor
    TypeMember = ClassTypeMember
    Using = CClassUsing
    Inherit = CClassInheritance

    def __init__(self,
                 name: str,
                 inherit_from: Union['CClassInheritance', List['CClassInheritance'], None] = None,
                 members: List[CClassMember] = None,
                 doc: Union['Doc', None] = None
                 ):
        super(CClass, self).__init__(
            name=name,
            doc=doc
        )
        if members is None:
            self.members = []
        else:
            self.members = members

        if inherit_from is None:
            self.inherit_from = []
        elif isinstance(inherit_from, list):
            self.inherit_from = inherit_from
        else:
            self.inherit_from = [inherit_from]

        for member in self.members:
            if isinstance(member, CClassConstructor):
                member.name = self.name
            member.in_space = self

    def declaration(self,
                    style: 'Style' = default_style,
                    semicolon: bool = True,
                    doc: bool = True,
                    from_space: 'CSpace' = None,
                    without_arguments: bool = False
                    ) -> str:
        self.style_checks(style)
        return f"class {self.name}{';' if semicolon else ''}"

    def _member_definition(self, style: 'Style') -> str:
        content = ""
        if style.class_members == Style.ClassMembers.inline_access_preserve_order:
            for i, member in enumerate(self.members):
                content += style.indent(
                    f"{style.new_line_token if i != 0 else ''}"
                    f"{member.doc_render(style)}"
                    f"{member.access.name}: "
                    f"{member.declaration(style, from_space=self, doc=False)}"
                    f"{style.new_line_token if i < len(self.members) - 1 else ''}",
                    obj="class_member"
                )
        if style.class_members == Style.ClassMembers.group_by_access_specified:
            access_contents = []
            for access in CClassAccess:
                access_members = [member for member in self.members if member.access.value == access.value]
                if len(access_members) > 0:
                    access_content = f"{access.name}:\n"

                    for member in access_members:
                        access_content += style.indent(member.declaration(from_space=self) + '\n', "class_member")
                    access_content = access_content.rstrip('\n')

                    access_content = style.indent(access_content, "class_access")
                    access_contents.append(access_content)
            for access_content in access_contents:
                content += access_content + ('\n' if access_content is not access_contents[-1] else '')

        return content

    @property
    def _inheritance_definition(self) -> str:
        content = ":"
        for inherit in self.inherit_from:
            content += f" {inherit.access.name} {inherit.cls.name},"

        return content.rstrip(",")

    def definition(self, style: 'Style' = default_style) -> str:
        self.style_checks(style)

        return (
            f"{self.doc_render(style)}"
            f"{self.declaration(style=style, semicolon=False)}"
            f"{self._inheritance_definition}"
            f"{style.bracket_open('class')}"
            f"{self._member_definition(style)}"
            f"{style.bracket_close('class')};"
        )

    def all_members_definition(self) -> List[str]:
        return [
            member.definition()
            for member
            in self.members
            if isinstance(member, CClassConstructor) or isinstance(member, CClassMethod)
        ]

    def style_checks(self, style: 'Style') -> None:
        pass

    @property
    def constructor(self):
        for member in self.members:
            if isinstance(member, CClassConstructor):
                return member
