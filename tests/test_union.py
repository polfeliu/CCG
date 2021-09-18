from ccg import CUnionDef, CVariable, CArray
from ccg.Ctypes import *
from common_style import style


def test_union():
    example_union_def = CUnionDef("TExamplestruct", members=[
        CVariable("i8Title", Cint8),
        CVariable("i8Asdf", Cint8),
        CArray("i8Name", type=Cint8, length=3),
        CVariable("tNestedstruct", type=CUnionDef(
            # This union def is anonymous
            members=[
                CVariable("i64Qwer", Cint64),
            ]),
                  ),

        CVariable("tNestedstruct2", type=CUnionDef(
            "TNestedstruct2",
            members=[
                CVariable("i64Qwer", Cint64),
            ]).union,  # Reference the union type, not the def, and its not declared inplace
                  )
    ])

    # Declaration of struct definition
    print(example_union_def.declaration(style))

    # Can declare a struct with a variable in the same sentence
    print(CVariable("tInst", type=example_union_def).declaration(style=style))

    # Or assume the struct is already declared and use it as type
    print(CVariable("tInst", type=example_union_def.union).declaration(style=style))

    # Can do a typedef of the struct with the declaration of the struct inplace
    print(example_union_def.type("TMyStruct").typedef(style))

    # Or the struct is already declared and can be typedefed afterwards
    print(example_union_def.union.type("TMyStruct").typedef(style))


if __name__ == "__main__":
    test_union()
