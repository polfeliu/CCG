from ccg import Struct, StructMember
from ccg.types import *


def test_struct():
    ExampleStruct = Struct("examplestruct_s", members=[
        StructMember(Variable("title", Int8)),
        StructMember(Variable("asdf", Int8), bitfield=3),
        StructMember(Array("name", type=Int8, length=3, inplace_declaration=True)),
        StructMember(
            Variable("nestedstruct", inplace_declaration=True, type=Struct(
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


if __name__ == "__main__":
    test_struct()
