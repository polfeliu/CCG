from ccg import *


def test_types():
    var = CVariable(
        c_type=Cint8,
        name="i8Mycustomint",
        initial_value=CCast(Cuint8, CExpressionFreeStyle("1")),
        doc=Doc("My Custom Int8")
    )
    print(var.declaration())


if __name__ == "__main__":
    test_types()
