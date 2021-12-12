from ccg import *


def test_class():
    enum = CEnum([
        CEnum.Member("first"),
        CEnum.Member("second"),
        CEnum.Member("third", value=CLiteral(10))
    ])

    print(enum.declare().render())


if __name__ == "__main__":
    test_class()
