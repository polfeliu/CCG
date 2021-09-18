from typing import List
from .types import *
from ccg import CVariable

from .style import default_style


class CFunctionArgument(CVariable):

    def __init__(self, name: str, type: 'CGenericType', default=None):
        super(CFunctionArgument, self).__init__(name, type)
        self.default = default


class CFunction:

    def __init__(self, name, return_type: CGenericType = None, arguments: List[CFunctionArgument] = None, content=None):
        if arguments is None:
            self.arguments = []
        else:
            self.arguments = arguments

        self.name = name
        self.return_type = return_type
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

    def _argument_list(self, include_defaults=False):
        argumentlist = ""
        for argument in self.arguments:
            default = ''
            if argument.default is not None and include_defaults:
                default = f" = {argument.default}"
            argumentlist += f"{argument.type.type_name} {argument.name}{default}, "
        return argumentlist.rstrip(", ")

    def prototype(self, style: 'Style' = default_style, semicolon: bool = True):
        return (
            f"{self.return_type.type_name} "
            f"{style.vnew_line_function_prototype_after_type}"
            f"{self.name}"
            f"{style.vspace_function_after_name_prototype}"
            f"({self._argument_list(include_defaults=True)})"
            f"{';' if semicolon else ''}"
        )

    def declaration(self, style: 'Style' = default_style):
        return (
            f"{self.return_type.type_name} "
            f"{self.name}"
            f"{style.vspace_function_after_name_declaration}"
            f"({self._argument_list()})"
            f"{style.bracket_open('function')}"
            f"{self.content if self.content is not None else ''}"
            f"{style.bracket_close('function')};"
        )
