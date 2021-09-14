from ccg import CStruct, StructMember, CVariable, CArray
from ccg.types import *
from common_style import style


def test_struct():
    ExampleStruct = CStruct("TExamplestruct", members=[
        StructMember(CVariable("i8Title", int8)),
        StructMember(CVariable("i8Asdf", int8), bitfield=3),
        StructMember(CArray("i8Name", type=int8, length=3)),
        StructMember(
            CVariable("tNestedstruct", inplace_declaration=True, type=CStruct(
                type_name="TNestedstruct",
                members=[
                    StructMember(CVariable("i64Qwer", int64)),
                ]),
                      )
        )
    ])

    print(CVariable("tInst", type=ExampleStruct, inplace_declaration=False).declaration(style=style))
    print(CArray("tInst", type=ExampleStruct, length=10, inplace_declaration=True).declaration(style=style))
    print(ExampleStruct.typedef('structtype'))



if __name__ == "__main__":
    test_struct()
