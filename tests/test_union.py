from ccg import CUnion, CVariable, CArray
from ccg.types import *


def test_union():
    ExampleUnion = CUnion(
        type_name="asdf",
        members=[
            CVariable("var1", int64),
            CArray("asdf", int64, length=12)
        ]
    )

    print(ExampleUnion.declaration())


if __name__ == "__main__":
    test_union()
