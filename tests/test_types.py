from ccg import Variable, Array
from ccg.types import *


def test_types():
    var = Variable(
        type=Int8,
        name="mycustomint"
    )
    print(var.declaration())

    print(Int8().typedef('mycustomtype'))

    array = Array(
        type=Int8,
        name="asdf",
        length=10
    )

    print(array.declaration())


if __name__ == "__main__":
    test_types()
