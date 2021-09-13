from typing import List
from .types import *


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

    def declaration(self):
        argumentlist = ""
        for argument in self.arguments:
            argumentlist += f"{argument.type.type_name} {argument.name}, "
        argumentlist = argumentlist.rstrip(", ")

        return (
            f"{self.return_type.type_name} {self.name}({argumentlist}){{\n"
            f"{self.content if self.content is not None else ''}"
            f"}}"
        )

    def prototype(self):
        pass
