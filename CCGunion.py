from typing import List
from textwrap import indent
from CCGtypes import *

class UnionMember:

    def __init__(self, name: str, type):
        self.type = type
        self.name = name

    type = None
    name: str

    def declaration(self):
        return (
            f"{self.type.declaration(self.name, semicolon=False)};"
        )


class Union(BasicType):

    def __init__(self, typename: str, members: List[UnionMember]):
        self.typename = typename
        self.members = members

    members: List[UnionMember] = []

    def declaration(self, name=None, semicolon=True):
        members = ""
        for member in self.members:
            members += indent(member.declaration(), '\t') + "\r\n"
        return (
            f"union {self.typename}{{\r\n"
            f"{members}"
            f"}}{name if name is not None else ''}{';' if semicolon else ''}"
        )

    def typedef(self, name, inplace_declaration=True):
        return (
            f"typedef {self.declaration(name = name, semicolon=False) if inplace_declaration else self.typename + ' ' + name};"
        )
        print(name)


if __name__ == "__main__":

    ExampleStruct = Union("exampleunion_u", members=[
        UnionMember("title", Int8()),
        UnionMember("example", Array(type=Int8, length=3)),
        UnionMember("Nestedunion",
             Union("nestedunion_u", members=[
                UnionMember("hello", Int8())
             ])
        )
    ])

    print(ExampleStruct.declaration())
    print(ExampleStruct.typedef('type', inplace_declaration=True))
