from ccg import CVariable, CArray
from ccg.Ctypes import *
from common_style import style


def test_types():
    var = CVariable(
        c_type=Cint8,
        name="i8Mycustomint",
        initial_value=4
    )
    print(var.declaration(style=style))

    try:
        var = CVariable(
            c_type=Cuint8,
            name="i8Mycustomint_invalid",
            initial_value=500
        )
    except Exception as ex:
        print(ex)

    array = CArray(
        c_type=Cint8,
        name="i8Asdf",
        length=10
    )

    print(array.declaration(style=style))

    # New type
    custom = Cint8.type('TMyCustomType')
    var = CVariable(
        c_type=custom,
        name="tMyVar"
    )

    print(custom.typedef(style=style))
    print(var.declaration(style=style))

    # Static
    var = CVariable(c_type=Cuint8, name="u8Var", static=True)
    print(var.declaration())

    # Static and const
    var = CVariable(c_type=Cuint8, name="u8Var", static=True, const=True)
    print(var.declaration())

    # Constexpr
    var = CVariable(c_type=Cuint8, name="u8Var", constexpr=True)
    print(var.declaration())


if __name__ == "__main__":
    test_types()
