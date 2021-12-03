from ccg import *
from os.path import join, dirname


# TODO Create example instead of text

def test_file():
    function = CFunction(
        name="examplefun",
        return_type=Cuint32,
        static=True,
        arguments=[
            CFunction.Argument(name="first", c_type=Cuint32, doc=Doc("First argument")),
            CFunction.Argument(name="second", c_type=Cdouble, default=CLiteral(2), doc=Doc("Second Argument"))
        ],
        doc=Doc("Awesome function", "This function is awesome because it does marvellous things",
                ret="returns a lucky number"),
        content=CStatements([
            CVariable("local_var", Cint8).declare()
        ])
    )

    var = CVariable(
        c_type=Cint8,
        name="i8Mycustomint",
        initial_value=CCast(Cint8, CLiteral(12, c_type=Cuint8, literal_format=CLiteral.Format.decimal))
    )

    user_code_statement = UserSectionStatement("first")

    user_code_statement_2 = UserSectionStatement("second")

    file = File([
        var.declare(),
        user_code_statement,
        function.declare(),
        user_code_statement_2
    ])

    file.generate(join(dirname(__file__), "generated_code/test_file_output.c"))


if __name__ == "__main__":
    test_file()
