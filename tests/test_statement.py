from ccg import *


def test_statement():
    var = CVariable("u32My_var", Cuint32, initial_value=5)
    array = CArray("u8My_array", Cuint8, length=10)
    statements = CStatements([
        var.declare(),
        array.declare(),

        # Statements can also contain other statements
        CStatements([
            CVariable("u8Var", Cuint8, initial_value=3).declare()
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


if __name__ == "__main__":
    test_statement()
