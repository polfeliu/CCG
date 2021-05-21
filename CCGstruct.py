from typing import List

from CCGtypes import *


class StructMember:

    def __init__(self, type, name, bitfield=None):
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


class Struct:

    def __init__(self, tag):
        self.tag = tag

    tag: str
    members: List[StructMember] = []

    def declaration(self, name=None):
        members = ""
        for member in self.members:
            members += f"\t{member.declaration()}\r\n"
        return (
            f"struct {self.tag} {{\r\n"
            f"{members}"
            f"}};\r\n"
        )


if __name__ == "__main__":

    ExampleStruct = Struct("examplestruct")
    ExampleStruct.members.extend([
        StructMember(Int8(), "title", bitfield=6),
        StructMember(Array(type=Int8, length=3), "example")
    ])

    print(ExampleStruct.declaration())
