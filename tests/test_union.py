from ccg import *


def test_union():
    example_union_def = CUnionDef(
        "ExampleUnion",
        doc=Doc("Example Union", "This union has many schrodinger's cat members"),
        members=[
            CVariable("i8Title", Cint8, doc=Doc("Title")),
            CVariable("i8Asdf", Cint8, doc=Doc("Random variable")),
            CArray("i8Name", c_type=Cint8, length=3),
            CVariable("tNestedUnion", c_type=CUnionDef(
                # This union def is anonymous
                members=[
                    CVariable("i64Qwer", Cint64),
                ]),
                      ),

            CVariable("tNestedUnion2", c_type=CUnionDef(
                "TNestedUnion2",
                members=[
                    CVariable("i64Qwer", Cint64),
                ]).union,  # Reference the union type, not the def, and its not declared inplace
                      )
        ])

    # Declaration of union definition
    print(example_union_def.declaration())

    # Can declare a union with a variable in the same sentence
    print(CVariable("tInst", c_type=example_union_def).declaration())

    # Or assume the union is already declared and use it as type
    print(CVariable("tInst", c_type=example_union_def.union).declaration())

    # Can do a typedef of the union with the declaration of the union inplace
    print(example_union_def.type("TMyStruct").typedef())

    # Or the union is already declared and can be typedefed afterwards
    print(example_union_def.union.type("TMyStruct").typedef())


if __name__ == "__main__":
    test_union()
