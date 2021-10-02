from typing import TYPE_CHECKING, List, Union

from ccg import CVariable
from .Cstatement import Cdeclaration
from .Ctypes import CGenericType, CVoidType, CNoType
from .style import default_style

if TYPE_CHECKING:
    from .style import Style
    from .Cnamespace import CSpace


class CFunctionArgument(CVariable):

    def __init__(self, name: str, c_type: 'CGenericType', default=None, auto_hungarize: bool = False):
        # TODO what python type should default be??. Maybe types should have a TypeValue object, that validates the
        #  type, or in case of structs, fills the members
        super(CFunctionArgument, self).__init__(name, c_type, auto_hungarize=auto_hungarize)
        self.default = default
        if default is not None:
            if self.c_type.check_value(self._initial_value) is not True:
                raise ValueError(f"Default value [{default}] does not fit type [{self.c_type.name}]")


class CFunction(CGenericType):
    # TODO This should also be a type, when asked, it's type name it should return a C pointer

    Argument = CFunctionArgument

    def __init__(self,
                 name: str,
                 return_type: CGenericType = CVoidType,
                 arguments: Union[List[CFunctionArgument], None] = None,
                 content=None,
                 in_space: Union['CSpace', None] = None,
                 static: bool = False
                 ):
        super(CFunction, self).__init__(
            name=name,
            hungarian_prefixes=[],
            in_space=in_space
        )
        if arguments is None:
            self.arguments = []
        else:
            self.arguments = arguments

        self.return_type = return_type

        self.content = content  # TODO Change content for list of statements or something like
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
        argumentlist = ""
        if len(self.arguments) > 0:
            argumentlist = ""
            for argument in self.arguments:
                default = ''
                if argument.default is not None and include_defaults:
                    default = f" = {argument.default}"
                argumentlist += f"{argument.c_type.name} {argument.name}{default}, "
            argumentlist = argumentlist.rstrip(", ")
        else:
            if style.function_void_when_no_arguments:
                argumentlist = "void"

        return argumentlist

    def declaration(self, style: 'Style' = default_style, semicolon: bool = True, from_space: 'CSpace' = None,
                    without_arguments: bool = False) -> str:
        return (
            f"{'static ' if self.static else ''}"
            f"{self.return_type.name}"
            f"{' ' if self.return_type is not CNoType else ''}"
            f"{style.vnew_line_function_declaration_after_type}"
            f"{self.space_def(from_space)}"
            f"{self.name}"
            f"{style.vspace_function_after_name_declaration}"
            f"{'(' + self._argument_list(style=style, include_defaults=True) + ')' if without_arguments == False else ''}"
            f"{';' if semicolon else ''}"
        )

    def definition(self, style: 'Style' = default_style, from_space: 'CSpace' = None) -> str:
        return (
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

    def declare(self) -> Cdeclaration:
        return Cdeclaration(
            render_function=self.declaration
        )

    def define(self) -> Cdeclaration:
        return Cdeclaration(
            render_function=self.definition
        )