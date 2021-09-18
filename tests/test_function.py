from ccg import CFunction, CFunctionArgument
from ccg.types import *

from common_style import style


def test_function():
    f = CFunction(
        name="examplefun",
        return_type=Cuint32,
        arguments=[
            CFunctionArgument(name="first", type=Cuint32),
            CFunctionArgument(name="second", type=Cdouble, default=2)
        ]
    )

    print(f.prototype(style))
    print(f.declaration(style))


if __name__ == "__main__":
    test_function()
