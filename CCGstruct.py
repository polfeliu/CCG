from typing import List
from textwrap import indent
from CCGtypes import *


class StructMember:

    def __init__(self, name: str, type, bitfield=None):
        self.type = type
        self.name = name
        self.bitfield = bitfield

    type = None
    name: str
    bitfield: int

    def declaration(self):
        return (
            f"{self.type.declaration(self.name, semicolon=False)}{f': {self.bitfield}' if self.bitfield else '' };"
        )


class Struct(BasicType):

    def __init__(self, typename: str, members: List[StructMember]):
        self.typename = typename
        self.members = members

    members: List[StructMember] = []

    def declaration(self, name=None, semicolon=True):
        members = ""
        for member in self.members:
            members += indent(member.declaration(), '\t') + "\r\n"
        return (
            f"struct {self.typename}{{\r\n"
            f"{members}"
            f"}}{name if name is not None else ''}{';' if semicolon else ''}"
        )


if __name__ == "__main__":

    ExampleStruct = Struct("examplestruct_s", members=[
        StructMember("title", Int8(), bitfield=6),
        StructMember("example", Array(type=Int8, length=3)),
        StructMember("Nestedstruct",
             Struct("nestedstruct_s", members=[
                StructMember("hello", Int8(), bitfield=6)
             ])
        )
    ])

    print(ExampleStruct.declaration())
