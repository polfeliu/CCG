from ccg import CFunction
from ccg.Ctypes import *

from common_style import style


def test_function():
    f = CFunction(
        name="examplefun",
        return_type=Cuint32,
        arguments=[
            CFunction.Argument(name="first", c_type=Cuint32),
            CFunction.Argument(name="second", c_type=Cdouble, default=2)
        ]
    )

    print(f.declaration(style))
    print(f.definition(style))

    f.static = True

    print(f.declaration(style))
    print(f.definition(style))


if __name__ == "__main__":
    test_function()
