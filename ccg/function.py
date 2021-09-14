from typing import List
from .types import *

from .style import default_style


class CFunctionArgument:

    def __init__(self, name, type):
        self.name = name
        self.type = type

    name: str = None
    type = None


class CFunction:

    def __init__(self, name, return_type=None, arguments: List[CFunctionArgument] = None, content=None):
        if arguments is None:
            self.arguments = []
        else:
            self.arguments = arguments

        self.name = name
        self.return_type = return_type
        self.content = content

    name: str
    return_type: CGenericType = None
    arguments: List[CFunctionArgument]
    content = None  # TODO Change content for list of statements or something like that

    def declaration(self, style: 'Style' = default_style):
        argumentlist = ""
        for argument in self.arguments:
            argumentlist += f"{argument.type.type_name} {argument.name}, "
        argumentlist = argumentlist.rstrip(", ")

        return (
            f"{self.return_type.type_name} {self.name}({argumentlist})"
            f"{style._new_line_function_bracket_open_before}{{{style._new_line_function_bracket_open_after}"
            f"{self.content if self.content is not None else ''}"
            f"{style._new_line_function_bracket_close_before}}}{style._new_line_function_bracket_close_after}"
        )

    def prototype(self, style: Union['Style', None] = None):
        pass
