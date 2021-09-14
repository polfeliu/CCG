from ccg import CVariable, CArray
from ccg.types import *
from common_style import style


def test_types():
    var = CVariable(
        type=Cint8,
        name="i8Mycustomint"
    )
    print(var.declaration(style=style))

    array = CArray(
        type=Cint8,
        name="i8Asdf",
        length=10
    )

    print(array.declaration(style=style))

    # New type
    custom = Cint8.type('TMyCustomType')
    var = CVariable(
        type=custom,
        name="tMyVar"
    )

    print(custom.typedef(style=style))
    print(var.declaration(style=style))


if __name__ == "__main__":
    test_types()
