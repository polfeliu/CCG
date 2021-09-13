from ccg import Struct, StructMember, Variable, Array
from ccg.types import *


def test_struct():
    ExampleStruct = Struct("examplestruct_s", members=[
        StructMember(Variable("title", Int8)),
        StructMember(Variable("asdf", Int8), bitfield=3),
        StructMember(Array("name", type=Int8, length=3)),
        StructMember(
            Variable("nestedstruct", inplace_declaration=True, type=Struct(
                type_name="nestedstruct_s",
                members=[
                    StructMember(Variable("qwer", Int64)),
                ]),
                     )
        )
    ])

    print(Variable("inst", type=ExampleStruct, inplace_declaration=False).declaration())
    print(Array("inst", type=ExampleStruct, length=10, inplace_declaration=True).declaration())
    print(ExampleStruct.typedef('structtype'))



if __name__ == "__main__":
    test_struct()
