from ccg import Function, FunctionArgument
from ccg.types import *


def test_function():
    f = Function(
        name="examplefun",
        return_type=Uint32,
        arguments=[
            FunctionArgument(name="asdf", type=Uint32),
            FunctionArgument(name="qwerw", type=double)
        ]
    )

    print(f.declaration())
    print(f.prototype())


if __name__ == "__main__":
    test_function()
