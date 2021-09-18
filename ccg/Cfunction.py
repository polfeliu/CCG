from typing import TYPE_CHECKING, List, Union
from ccg import CVariable

from .style import default_style
from .Ctypes import CGenericType, CVoidType

if TYPE_CHECKING:
    from .style import Style


class CFunctionArgument(CVariable):

    def __init__(self, name: str, type: 'CGenericType', default=None):
        # TODO what python type should default be??. Maybe types should have a TypeValue object, that validates the
        #  type, or in case of structs, fills the members
        super(CFunctionArgument, self).__init__(name, type)
        self.default = default
        if default is not None:
            if self.type.check_value(self._initial_value) is not True:
                raise ValueError(f"Default value [{default}] does not fit type [{self.type.name}]")


class CFunction(
    CGenericType):  # TODO This should also be a type, when asked, it's type name it should return a C pointer

    Argument = CFunctionArgument

    def __init__(self,
                 name: str,
                 return_type: Union['CGenericType', None] = None,
                 arguments: Union[List[CFunctionArgument], None] = None,
                 content=None,
                 in_space: Union['CSpace', None] = None
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
        if self.return_type is None:
            self.return_type = CVoidType

        self.content = content  # TODO Change content for list of statements or something like

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

    def _argument_list(self, include_defaults: bool = False) -> str:
        argumentlist = ""
        for argument in self.arguments:
            default = ''
            if argument.default is not None and include_defaults:
                default = f" = {argument.default}"
            argumentlist += f"{argument.type.name} {argument.name}{default}, "
        return argumentlist.rstrip(", ")

    def declaration(self, style: 'Style' = default_style, semicolon: bool = True, from_space: 'CSpace' = None) -> str:
        return (
            f"{self.return_type.name} "
            f"{style.vnew_line_function_prototype_after_type}"
            f"{self.space_def(from_space)}"
            f"{self.name}"
            f"{style.vspace_function_after_name_prototype}"
            f"({self._argument_list(include_defaults=True)})"
            f"{';' if semicolon else ''}"
        )

    def definition(self, style: 'Style' = default_style, from_space: 'CSpace' = None) -> str:
        return (
            f"{self.return_type.name} "
            f"{self.space_def(from_space)}"
            f"{self.name}"
            f"{style.vspace_function_after_name_declaration}"
            f"({self._argument_list()})"
            f"{style.bracket_open('function')}"
            f"{self.content if self.content is not None else ''}"
            f"{style.bracket_close('function')};"
        )
