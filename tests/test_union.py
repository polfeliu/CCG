from ccg import CUnion, CVariable, CArray
from ccg.types import *


def test_union():
    ExampleUnion = CUnion(
        type_name="asdf",
        members=[
            CVariable("var1", Cint64),
            CArray("asdf", Cint64, length=12)
        ]
    )

    print(ExampleUnion.declaration())


if __name__ == "__main__":
    test_union()
