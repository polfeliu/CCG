from ccg import *


def test_types():
    var = CVariable(
        c_type=Cint8,
        name="i8Mycustomint",
        initial_value=4,
        doc=Doc("My Custom Int8")
    )
    # print(var.declaration())

    try:
        var = CVariable(
            c_type=Cuint8,
            name="i8Mycustomint_invalid",
            initial_value=500,
        )
    except Exception as ex:
        pass  # print(ex)

    array = CArray(
        c_type=Cint8,
        name="i8Array",
        length=10,
        doc=Doc("My Custom Int8 Array", "This array is awesome because it can hold 10 int8")
    )

    # print(array.declaration())

    # New type
    custom = Cint8.type('TMyCustomType')
    var = CVariable(
        c_type=custom,
        name="tMyVar"
    )

    print(custom.typedef(doc=Doc("My Custom Type", "Awesome type because I have defined it")).render())
    # print(var.declaration())

    # Static
    var = CVariable(c_type=Cuint8, name="u8Var", static=True)
    # print(var.declaration())

    # Static and const
    var = CVariable(c_type=Cuint8, name="u8Var", static=True, const=True)
    # print(var.declaration())

    # Constexpr
    var = CVariable(c_type=Cuint8, name="u8Var", constexpr=True)
    # print(var.declaration())


if __name__ == "__main__":
    test_types()
