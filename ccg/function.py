from typing import List
from .types import *
from ccg import CVariable

from .style import default_style




class CFunction:

    def __init__(self, name, return_type=None, arguments: List[CVariable] = None, content=None):
        if arguments is None:
            self.arguments = []
        else:
            self.arguments = arguments

        self.name = name
        self.return_type = return_type
        self.content = content

    name: str
    return_type: CGenericType = None
    arguments: List[CVariable]
    content = None  # TODO Change content for list of statements or something like that

    def _argument_list(self):
        argumentlist = ""
        for argument in self.arguments:
            argumentlist += f"{argument.type.type_name} {argument.name}, "
        return argumentlist.rstrip(", ")

    def prototype(self, style: 'Style' = default_style, semicolon: bool = True):
        return (
            f"{self.return_type.type_name} "
            f"{style._new_line_function_prototype_type}"
            f"{self.name}"
            f"{style._space_function_after_name_prototype}"
            f"({self._argument_list()})"
            f"{';' if semicolon else ''}"
        )

    def declaration(self, style: 'Style' = default_style):
        return (
            f"{self.return_type.type_name} "
            f"{self.name}"
            f"{style._space_function_after_name_declaration}"
            f"({self._argument_list()})"
            f"{style._new_line_function_bracket_open_before}{{{style._new_line_function_bracket_open_after}"
            f"{self.content if self.content is not None else ''}"
            f"{style._new_line_function_bracket_close_before}}}{style._new_line_function_bracket_close_after};"
        )
