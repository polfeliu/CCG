from ccg import CVariable, CArray, CFunction
from ccg import CStatements, CDeclarations
from ccg.Ctypes import *


def test_statement():
    var = CVariable("u32My_var", Cuint32, initial_value=5)
    array = CArray("u8My_array", Cuint8, length=10)
    statements = CStatements([
        # Cstatements only allow variable declaration and manipulation
        var.declare(),
        array.declare()
    ])

    fun = CFunction("my_fun")

    declarations = CDeclarations([
        # Declarations include declarations of variable, function, class... etc
        fun.declare(),
        fun.define()
    ])

    # TODO nested

    print(statements.render())
    print(declarations.render())


if __name__ == "__main__":
    test_statement()
