from typing import TYPE_CHECKING, List, Any, Optional

from ccg import CVariable
from .Cstatement import CDeclaration
from .Ctypes import CGenericType, CVoidType, CNoType, CItemDefinable
from .style import default_style

if TYPE_CHECKING:
    from .style import Style
    from .Cnamespace import CSpace
    from .doc import Doc


class CFunctionArgument(CVariable):

    def __init__(self,
                 name: str,
                 c_type: 'CGenericType',
                 default: Any = None,
                 auto_hungarize: bool = False,
                 doc: Optional['Doc'] = None
                 ):
        super(CFunctionArgument, self).__init__(
            name=name,
            c_type=c_type,
            auto_hungarize=auto_hungarize
        )
        self.doc = doc
        self.default = default
        if default is not None:
            if self.c_type.check_value(self._initial_value) is not True:
                raise ValueError(f"Default value [{default}] does not fit type [{self.c_type.name}]")


class CFunction(CGenericType, CItemDefinable):
    Argument = CFunctionArgument

    def __init__(self,
                 name: str,
                 return_type: CGenericType = CVoidType,
                 arguments: Optional[List[CFunctionArgument]] = None,
                 content=None,
                 in_space: Optional['CSpace'] = None,
                 static: bool = False,
                 doc: Optional['Doc'] = None
                 ):
        super(CFunction, self).__init__(
            name=name,
            hungarian_prefixes=[],
            in_space=in_space,
            doc=doc
        )
        if arguments is None:
            self.arguments = []
        else:
            self.arguments = arguments

        self.return_type = return_type

        self.content = content
        self.static = static

        # Check that non-default arguments are after default arguments
        defaults_started = False
        for argument in self.arguments:
            if not defaults_started:
                if argument.default is not None:
                    defaults_started = True
            else:
                if argument.default is None:
                    raise SyntaxError(f"Argument [{argument.name}] without default follows arguments with defaults"
                                      f"on function [{self.name}]")

    def _argument_list(self, style: 'Style', include_defaults: bool = False) -> str:
        argument_list = ""
        if len(self.arguments) > 0:
            argument_list = ""
            for argument in self.arguments:
                default = ''
                if argument.default is not None and include_defaults:
                    default = f" = {argument.default}"
                argument_list += f"{argument.c_type.name} {argument.name}{default}, "
            argument_list = argument_list.rstrip(", ")
        else:
            if style.function_void_when_no_arguments:
                argument_list = "void"

        return argument_list

    def declaration(self,
                    style: 'Style' = default_style,
                    semicolon: bool = True,
                    doc: bool = True,
                    from_space: 'CSpace' = None,
                    without_arguments: bool = False
                    ) -> str:
        return (
            f"{self.doc_render(style) if doc else ''}"
            f"{'static ' if self.static else ''}"
            f"{self.return_type.name}"
            f"{' ' if self.return_type is not CNoType else ''}"
            f"{style.vnew_line_function_declaration_after_type}"
            f"{self.space_def(from_space)}"
            f"{self.name}"
            f"{style.vspace_function_after_name_declaration}"
            f"{'(' + self._argument_list(style, include_defaults=True) + ')' if without_arguments == False else ''}"
            f"{';' if semicolon else ''}"
        )

    def doc_render(self, style: 'Style') -> str:
        if self.doc is None:
            return ""

        content = []
        for argument in self.arguments:
            content.append(
                f"{style.doxygen_command('param')} "
                f"{argument.name} "
                f"{argument.doc.brief if argument.doc is not None else ''}"
            )
        if self.return_type != CVoidType:
            if self.doc.ret is None:
                raise AttributeError(f"Missing return value documentation for function with non void return value")
            else:
                content.append(f"{style.doxygen_command('return')} {self.doc.ret}")

        return self.doc.render(style, content=content)

    def definition(self,
                   style: 'Style' = default_style,
                   from_space: 'CSpace' = None,
                   doc: bool = False
                   ) -> str:
        return (
            f"{self.doc_render(style) if doc else ''}"
            f"{'static ' if self.static else ''}"
            f"{self.return_type.name}"
            f"{' ' if self.return_type is not CNoType else ''}"
            f"{self.space_def(from_space)}"
            f"{self.name}"
            f"{style.vspace_function_after_name_definition}"
            f"({self._argument_list(style=style)})"
            f"{style.bracket_open('function')}"
            f"{self.content if self.content is not None else ''}"
            f"{style.bracket_close('function')};"
        )

    def declare(self) -> CDeclaration:
        return CDeclaration(
            render_function=self.declaration
        )

    def define(self) -> CDeclaration:
        return CDeclaration(
            render_function=self.definition
        )
