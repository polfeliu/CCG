from ccg import *


def test_class():
    enum = CEnum(
        members=[
            CEnum.Member("first"),
            CEnum.Member("second"),
            CEnum.Member("third", value=CLiteral(10))
        ],
        name="my_enum",
        doc=Doc("Enumeration Example", "contains members")
    )

    print(enum.declare().render())

    enum = CEnum(
        members=[
            CEnum.Member("first"),
            CEnum.Member("second"),
            CEnum.Member("third", value=CLiteral(10))
        ],
        name="my_enum",
        key=CEnum.Key.enum_class,
        base_type=Cuint16,
        in_space=CNamespace("my_ns"),
        doc=Doc("Enumeration Example", "contains members")
    )

    print(enum.declare().render())


if __name__ == "__main__":
    test_class()
