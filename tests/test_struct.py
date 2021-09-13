from ccg import CStruct, StructMember, CVariable, CArray
from ccg.types import *


def test_struct():
    ExampleStruct = CStruct("examplestruct_s", members=[
        StructMember(CVariable("title", int8)),
        StructMember(CVariable("asdf", int8), bitfield=3),
        StructMember(CArray("name", type=int8, length=3)),
        StructMember(
            CVariable("nestedstruct", inplace_declaration=True, type=CStruct(
                type_name="nestedstruct_s",
                members=[
                    StructMember(CVariable("qwer", int64)),
                ]),
                      )
        )
    ])

    print(CVariable("inst", type=ExampleStruct, inplace_declaration=False).declaration())
    print(CArray("inst", type=ExampleStruct, length=10, inplace_declaration=True).declaration())
    print(ExampleStruct.typedef('structtype'))



if __name__ == "__main__":
    test_struct()
