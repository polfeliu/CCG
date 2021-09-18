from ccg import CStructDef, CVariable, CArray
from ccg.Ctypes import *
from common_style import style


def test_struct():
    # Struct definition
    example_struct_def = CStructDef("TExamplestruct", members=[
        CStructDef.Member(CVariable("i8Title", Cint8)),
        CStructDef.Member(CVariable("i8Asdf", Cint8), bitfield=3),
        CStructDef.Member(CArray("i8Name", c_type=Cint8, length=3)),
        CStructDef.Member(
            CVariable("tNestedstruct", c_type=CStructDef(
                # This struct def is anonymous
                members=[
                    CStructDef.Member(CVariable("i64Qwer", Cint64)),
                ]),
                      )
        ),

        CStructDef.Member(
            CVariable("tNestedstruct2", c_type=CStructDef(
                "TNestedstruct2",
                members=[
                    CStructDef.Member(CVariable("i64Qwer", Cint64)),
                ]).struct,  # Reference the struct type, not the def, and its not declared inplace
                      )
        )
    ])

    # Declaration of struct definition
    print(example_struct_def.declaration(style))

    # Can declare a struct with a variable in the same sentence
    print(CVariable("tInst", c_type=example_struct_def).declaration(style=style))

    # Or assume the struct is already declared and use it as type
    print(CVariable("tInst", c_type=example_struct_def.struct).declaration(style=style))

    # Can do a typedef of the struct with the declaration of the struct inplace
    print(example_struct_def.type("TMyStruct").typedef(style))

    # Or the struct is already declared and can be typedefed afterwards
    print(example_struct_def.struct.type("TMyStruct").typedef(style))


if __name__ == "__main__":
    test_struct()
