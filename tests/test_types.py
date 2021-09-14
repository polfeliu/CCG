from ccg import CVariable, CArray
from ccg.types import *
from common_style import style


def test_types():
    var = CVariable(
        type=int8,
        name="i8Mycustomint"
    )
    print(var.declaration(style=style))

    print(int8.typedef('mycustomtype'))

    array = CArray(
        type=int8,
        name="i8Asdf",
        length=10
    )

    print(array.declaration(style=style))


if __name__ == "__main__":
    test_types()
