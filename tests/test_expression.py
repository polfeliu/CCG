from ccg import *


def test_expression():
    # Cast and Literals
    var = CVariable(
        c_type=Cint8,
        name="i8Mycustomint",
        initial_value=CCast(Cint8, CLiteral(12, c_type=Cuint8, literal_format=CLiteral.Format.decimal))
    )
    print(var.declaration())

    var.c_type = Cuint8
    var.initial_value = CCast(Cuint8, CLiteral(12, c_type=Cuint8, literal_format=CLiteral.Format.octal))
    print(var.declaration())

    var.initial_value = CCast(Cuint8, CLiteral(12, c_type=Cuint8, literal_format=CLiteral.Format.hexadecimal))
    print(var.declaration())

    var.initial_value = CCast(Cuint8, CLiteral(12, c_type=Cuint8, literal_format=CLiteral.Format.binary))
    print(var.declaration())

    var.c_type = Cfloat
    var.initial_value = CCast(Cfloat, CLiteral(12, c_type=Cfloat, literal_format=CLiteral.Format.float_decimals))
    print(var.declaration())

    var.initial_value = CCast(Cfloat, CLiteral(12, c_type=Cfloat, literal_format=CLiteral.Format.float_scientific))
    print(var.declaration())

    # Operators
    NOT = COperators.Logic.Not
    print(NOT(CLiteral(False)).render())

    SUM = COperators.Arithmetic.Sum
    PARENTHESES = COperators.Parentheses
    print(
        PARENTHESES(
            SUM(CLiteral(2), CLiteral(3))
        ).render()
    )

    ASSIGN = COperators.Assignment.Assign
    print(
        ASSIGN(
            CExpressionFreeStyle("a"),
            CLiteral(5)
        ).render()
    )


if __name__ == "__main__":
    test_expression()
