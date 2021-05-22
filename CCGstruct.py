from typing import List
from textwrap import indent
from CCGtypes import *


class StructMember():

    def __init__(self, variable, bitfield=None):
        self.variable = variable
        self.bitfield = bitfield

    def declaration(self):
        return (
            f"{self.variable.declaration(semicolon=False)}{f': {self.bitfield}' if self.bitfield else '' };"
        )


class Struct(BasicType):

    def __init__(self, typename: str, members: List[StructMember]):
        self.typename = typename
        self.members = members

    members: List[StructMember] = []

    def declaration(self, name=None, semicolon=True):
        members = ""
        for member in self.members:
            members += indent(member.declaration(), '\t') + "\n"
        return (
            f"struct {self.typename}{{\n"
            f"{members}"
            f"}}"
        )

    def typedef(self, name, inplace_declaration=True):
        return (
            f"typedef {self.declaration(name = name, semicolon=False) if inplace_declaration else self.typename + ' ' + name};"
        )


if __name__ == "__main__":

    ExampleStruct = Struct("examplestruct_s", members=[
        StructMember(Variable("title", Int8)),
        StructMember(Variable("asdf", Int8), bitfield=3),
        StructMember(Array("name", type=Int8, length=3)),
        StructMember(
            Variable("nestedstruct", inplace_declaration= True, type=Struct(
                typename="nestedstruct_s",
                members=[
                    StructMember(Variable("qwer", Int64)),
                ]),
             )
        )
    ])

    print(Variable("inst", type=ExampleStruct, inplace_declaration=True).declaration())
    print(Array("inst", type=ExampleStruct, length=10, inplace_declaration=True).declaration())

    print(ExampleStruct.typedef('structtype'))

    with open("example.txt", "w") as f:
        f.write(
            ExampleStruct.declaration()
        )
