from ccg import *


def test_statement():
    var = CVariable("u32My_var", Cuint32, initial_value=CLiteral(3))
    array = CArray("u8My_array", Cuint8, length=10)
    statements = CStatements([
        var.declare(),
        array.declare(),

        # Statements can also contain other statements
        CStatements([
            CVariable("u8Var", Cuint8, initial_value=CLiteral(3)).declare()
        ])
    ])

    fun = CFunction("my_fun")

    declarations = CDeclarations([
        # Declarations include declarations and definitions of variable, function, class... etc
        # But not other statements (if, while, ...)
        fun.declare(),
        fun.define()
    ])

    print(statements.render())
    print(declarations.render())

    c_if = CIf(
        CLiteral(True),
        [
            var.declare()
        ]
    ).ELSE_IF(
        CLiteral(False),
        [
            array.declare()
        ]
    ).ELSE(
        [
            var.declare()
        ]
    )

    print(c_if.render())

    c_switch = CSwitch(
        CExpressionFreeStyle('i'),
        [
            CSwitch.Case(
                CLiteral(1),
                [
                    var.declare()
                ]
            ),
            CSwitch.Default(
                [
                    array.declare()
                ]
            )
        ]
    )

    print(c_switch.render())

    c_while = CWhile(
        CExpressionFreeStyle('i < 3'),
        [
            var.declare(),
            CContinue()
        ]
    )

    print(c_while.render())

    c_do_while = CDoWhile(
        [
            var.declare(),
            CBreak()
        ],
        CLiteral(False)
    )

    print(c_do_while.render())

    c_empty_for = CFor(
        statements=[
            var.declare()
        ]
    )

    print(c_empty_for.render())

    c_for = CFor(
        initial=CStatementFreeStyle('i=0'),
        condition=CExpressionFreeStyle('i<10'),
        iteration=CExpressionFreeStyle('i++'),
        statements=[
            var.declare(),
            CReturn(var)
        ]
    )

    print(c_for.render())


if __name__ == "__main__":
    test_statement()
