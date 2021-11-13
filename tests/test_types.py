from ccg import *


def test_types():
    var = CVariable(
        c_type=Cint8,
        name="i8Mycustomint",
        initial_value=CLiteral(1),
        doc=Doc("My Custom Int8")
    )
    print(var.declare().render())

    array = CArray(
        c_type=Cint8,
        name="i8Array",
        length=10,
        doc=Doc("My Custom Int8 Array", "This array is awesome because it can hold 10 int8")
    )

    print(array.declare().render())

    # New type
    custom = Cint8.type('TMyCustomType')
    var = CVariable(
        c_type=custom,
        name="tMyVar"
    )

    print(custom.typedef(doc=Doc("My Custom Type", "Awesome type because I have defined it")).render())
    print(var.declare().render())

    # Static
    var = CVariable(c_type=Cuint8, name="u8Var", static=True)
    print(var.declare().render())

    # Static and const
    var = CVariable(c_type=Cuint8, name="u8Var", static=True, const=True)
    print(var.declare().render())

    # Constexpr
    var = CVariable(c_type=Cuint8, name="u8Var", constexpr=True)
    print(var.declare().render())


if __name__ == "__main__":
    test_types()
