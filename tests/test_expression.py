from ccg import *


def test_expression():
    # Cast and Literals
    var = CVariable(
        c_type=Cint8,
        name="i8Mycustomint",
        initial_value=CCast(Cint8, CLiteral(12, c_type=Cuint8, literal_format=CLiteral.Format.decimal))
    )
    print(var.declare().render())

    var.c_type = Cuint8
    var.initial_value = CCast(Cuint8, CLiteral(12, c_type=Cuint8, literal_format=CLiteral.Format.octal))
    print(var.declare().render())

    var.initial_value = CCast(Cuint8, CLiteral(12, c_type=Cuint8, literal_format=CLiteral.Format.hexadecimal))
    print(var.declare().render())

    var.initial_value = CCast(Cuint8, CLiteral(12, c_type=Cuint8, literal_format=CLiteral.Format.binary))
    print(var.declare().render())

    var.c_type = Cfloat
    var.initial_value = CCast(Cfloat, CLiteral(12, c_type=Cfloat, literal_format=CLiteral.Format.float_decimals))
    print(var.declare().render())

    var.initial_value = CCast(Cfloat, CLiteral(12, c_type=Cfloat, literal_format=CLiteral.Format.float_scientific))
    print(var.declare().render())

    # Operators
    NOT = COperators.Logic.Not
    print(NOT(CLiteral(False)).render())

    var = CVariable("u8Var", Cuint8)
    print(var.declare().render())

    ASSIGN = COperators.Assignment.Assign
    print(
        ASSIGN(
            var,  # Assign a value to that value
            CLiteral(5)
        ).render()
    )

    SUM = COperators.Arithmetic.Sum
    print(
        SUM(
            CLiteral(2),
            var  # Use a variable in a sum
        ).render()
    )

    PARENTHESES = COperators.Parentheses
    print(
        PARENTHESES(
            # Typical operations (sum, subtract...) can be done using python built-in operations
            var + CLiteral(2) - CLiteral(3) * CLiteral(4) / CLiteral(5) % CLiteral(6)
            << CLiteral(7) >> CLiteral(8) & CLiteral(True) | CLiteral(False)
            + PARENTHESES(
                -CLiteral(9)  # Unary minus
            )
            + PARENTHESES(
                +CLiteral(2)  # Unary Plus
            )
            + PARENTHESES(
                ~CLiteral(False)  # Invert
            )
        ).render()
    )


if __name__ == "__main__":
    test_expression()
