from ccg import CStructDef, CStruct, CStructMember, CVariable, CArray
from ccg.types import *
from common_style import style


def test_struct():
    # Struct definition
    ExampleStructDef = CStructDef("TExamplestruct", members=[
        CStructMember(CVariable("i8Title", Cint8)),
        CStructMember(CVariable("i8Asdf", Cint8), bitfield=3),
        CStructMember(CArray("i8Name", type=Cint8, length=3)),
        CStructMember(
            CVariable("tNestedstruct", type=CStructDef(
                "TNestedstruct",
                members=[
                    CStructMember(CVariable("i64Qwer", Cint64)),
                ]),
                      )
        ),

        CStructMember(
            CVariable("tNestedstruct2", type=CStructDef(
                "TNestedstruct2",
                members=[
                    CStructMember(CVariable("i64Qwer", Cint64)),
                ]).struct,  # Reference the struct type, not the def, and its not declared inplace
                      )
        )
    ])

    print(ExampleStructDef.declaration(style))

    # print(CVariable("tInst", type=ExampleStruct).declaration(style=style))
    # print(CArray("tInst", type=ExampleStruct, length=10, inplace_declaration=True).declaration(style=style))
    # print(ExampleStruct.typedef('structtype'))


if __name__ == "__main__":
    test_struct()
