from ccg import CStructDef, CStructMember, CVariable, CArray
from ccg.types import *
from common_style import style


def test_struct():
    # Struct definition
    example_struct_def = CStructDef("TExamplestruct", members=[
        CStructMember(CVariable("i8Title", Cint8)),
        CStructMember(CVariable("i8Asdf", Cint8), bitfield=3),
        CStructMember(CArray("i8Name", type=Cint8, length=3)),
        CStructMember(
            CVariable("tNestedstruct", type=CStructDef(
                # This struct def is anonymous
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

    # Declaration of struct definition
    print(example_struct_def.declaration(style))

    # Can declare a struct with a variable in the same sentence
    print(CVariable("tInst", type=example_struct_def).declaration(style=style))

    # Or assume the struct is already declared and use it as type
    print(CVariable("tInst", type=example_struct_def.struct).declaration(style=style))

    # Can do a typedef of the struct with the declaration of the struct inplace
    print(example_struct_def.type("TMyStruct").typedef(style))

    # Or the struct is already declared and can be typedefed afterwards
    print(example_struct_def.struct.type("TMyStruct").typedef(style))


if __name__ == "__main__":
    test_struct()
