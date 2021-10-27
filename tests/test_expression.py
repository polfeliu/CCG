from ccg import *


def test_expression():
    # Cast and Literals
    var = CVariable(
        c_type=Cint8,
        name="i8Mycustomint",
        initial_value=CCast(Cint8, CLiteral(12, c_type=Cuint8, literal_format=CLiteral.Format.decimal))
    )
    print(var.declaration())

    var.initial_value = CCast(Cuint8, CLiteral(12, c_type=Cuint8, literal_format=CLiteral.Format.octal))
    print(var.declaration())

    var.initial_value = CCast(Cuint8, CLiteral(12, c_type=Cuint8, literal_format=CLiteral.Format.hexadecimal))
    print(var.declaration())

    var.initial_value = CCast(Cuint8, CLiteral(12, c_type=Cuint8, literal_format=CLiteral.Format.binary))
    print(var.declaration())

    var.initial_value = CCast(Cfloat, CLiteral(12, c_type=Cfloat, literal_format=CLiteral.Format.float_decimals))
    print(var.declaration())

    var.initial_value = CCast(Cfloat, CLiteral(12, c_type=Cfloat, literal_format=CLiteral.Format.float_scientific))
    print(var.declaration())


if __name__ == "__main__":
    test_expression()
