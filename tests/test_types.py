from ccg import Style, Variable, Array
from ccg.types import *


def test_types():
    style = Style()
    style.check_hungarian = True

    var = Variable(
        type=Int8,
        name="i8Mycustomint"
    )
    print(var.declaration(style=style))

    print(Int8().typedef('mycustomtype'))

    array = Array(
        type=Int8,
        name="asdf",
        length=10
    )

    print(array.declaration(style=style))


if __name__ == "__main__":
    test_types()
