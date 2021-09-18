from ccg import CUnionDef, CUnion, CVariable, CArray
from ccg.types import *
from common_style import style


def test_union():
    ExampleUnionDef = CUnionDef("TExamplestruct", members=[
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
    print(ExampleUnionDef.declaration(style))

    # Can declare a struct with a variable in the same sentence
    print(CVariable("tInst", type=ExampleUnionDef).declaration(style=style))

    # Or assume the struct is already declared and use it as type
    print(CVariable("tInst", type=ExampleUnionDef.union).declaration(style=style))

    # Can do a typedef of the struct with the declaration of the struct inplace
    print(ExampleUnionDef.type("TMyStruct").typedef(style))

    # Or the struct is already declared and can be typedefed afterwards
    print(ExampleUnionDef.union.type("TMyStruct").typedef(style))

if __name__ == "__main__":
    test_union()
