from typing import List
from CCGtypes import *

class FunctionArgument:

    def __init__(self, name, type):
        self.name = name
        self.type = type

    name: str = None
    type = None

class Function:

    def __init__(self, name, return_type=None, arguments: List[FunctionArgument] = None, content=None):
        if arguments is None:
            self.arguments = []
        else:
            self.arguments = arguments

        self.name = name
        self.return_type = return_type
        self.content = content

    name: str
    return_type: GenericType = None
    arguments: List[FunctionArgument]
    content = None  # TODO Change content for list of statements or something like that

    def declaration(self):
        argumentlist = ""
        for argument in self.arguments:
            argumentlist += f"{argument.type.typename} {argument.name}, "
        argumentlist = argumentlist.rstrip(", ")

        return (
            f"{self.return_type.typename} {self.name}({argumentlist}){{\n"
            f"{self.content if self.content is not None else ''}"
            f"}}"
        )


    def prototype(self):
        pass

if __name__ == "__main__":
    from CCGtypes import Uint32
    f = Function(
        name="examplefun",
        return_type=Uint32,
        arguments=[
            FunctionArgument(name="asdf", type=Uint32),
            FunctionArgument(name="qwerw", type=Double)
        ]
        )

    print(f.declaration())