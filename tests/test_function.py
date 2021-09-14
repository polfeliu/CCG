from ccg import CFunction
from ccg import CVariable
from ccg.types import *

from common_style import style

def test_function():
    f = CFunction(
        name="examplefun",
        return_type=Cuint32,
        arguments=[
            CVariable(name="first", type=Cuint32),
            CVariable(name="second", type=Cdouble)
        ]
    )

    print(f.prototype(style))
    print(f.declaration(style))


if __name__ == "__main__":
    test_function()
