from ccg import *


def test_expression():
    var = CVariable(
        c_type=Cint8,
        name="i8Mycustomint",
        initial_value=CCast(Cfloat, CLiteral(12.0, c_type=Cfloat, literal_format=CLiteral.Format.float_scientific)),
        doc=Doc("My Custom Int8")
    )
    print(var.declaration())


if __name__ == "__main__":
    test_expression()
