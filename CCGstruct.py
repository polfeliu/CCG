from typing import List

from CCGtypes import *


class StructMember:

    def __init__(self, name, type, bitfield=None):
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
        StructMember("title", Int8(), bitfield=6),
        StructMember("example", Array(type=Int8, length=3))
    ])

    print(ExampleStruct.declaration())
