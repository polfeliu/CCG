from ccg import *

from common_style import style


def test_function():
    f = CFunction(
        name="examplefun",
        return_type=Cuint32,
        arguments=[
            CFunction.Argument(name="first", c_type=Cuint32, doc=Doc("First argument")),
            CFunction.Argument(name="second", c_type=Cdouble, default=2, doc=Doc("Second Argument"))
        ],
        doc=Doc("Awesome function", "This function is awesome because it does marvellous things",
                ret="returns a lucky number")
    )

    print(f.declaration(style))
    print(f.definition(style))

    f.static = True

    print(f.declaration(style))
    print(f.definition(style))


if __name__ == "__main__":
    test_function()
