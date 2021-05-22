from typing import List
from textwrap import indent
from CCGtypes import *

class Union(BasicType):

    def __init__(self, typename: str, members):
        self.typename = typename
        self.members = members

    def declaration(self, name=None, semicolon=True):
        members = ""
        for member in self.members:
            members += indent(member.declaration(), '\t') + "\n"
        return (
            f"union {self.typename}{{\n"
            f"{members}"
            f"}}"
        )

    def typedef(self, name, inplace_declaration=True):
        return (
            f"typedef {self.declaration(name = name, semicolon=False) if inplace_declaration else self.typename + ' ' + name};"
        )


if __name__ == "__main__":


    ExampleUnion = Union(
        typename="asdf",
        members=[
            Variable("var1", Int64),
            Array("asdf", Int64, length=12)
        ]
    )

    print(ExampleUnion.declaration())