from ccg import *


def test_types():
    var = CVariable(
        c_type=Cint8,
        name="i8Mycustomint",
        initial_value=CCast(Cuint8, CLiteral(12, c_type=Cuint8, literal_format=CLiteral.Format.binary)),
        doc=Doc("My Custom Int8")
    )
    print(var.declaration())


if __name__ == "__main__":
    test_types()
