from ccg import CFunction, CFunctionArgument
from ccg.types import *

from common_style import style

def test_function():
    f = CFunction(
        name="examplefun",
        return_type=uint32,
        arguments=[
            CFunctionArgument(name="first", type=uint32),
            CFunctionArgument(name="second", type=double)
        ]
    )

    print(f.declaration(style))
    print(f.prototype(style))


if __name__ == "__main__":
    test_function()
