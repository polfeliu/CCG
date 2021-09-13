from ccg import Union
from ccg.types import *


def test_union():
    ExampleUnion = Union(
        typename="asdf",
        members=[
            Variable("var1", Int64),
            Array("asdf", Int64, length=12)
        ]
    )

    print(ExampleUnion.declaration())


if __name__ == "__main__":
    test_union()
