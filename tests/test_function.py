from ccg import *


def test_function():
    f = CFunction(
        name="examplefun",
        return_type=Cuint32,
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

    print(f.declare().render())
    print(f.define().render())

    f.static = True

    print(f.declare().render())
    print(f.define().render())


if __name__ == "__main__":
    test_function()
