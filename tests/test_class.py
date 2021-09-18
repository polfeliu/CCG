from ccg import CClass, CFunction
from ccg.Ctypes import *
from common_style import style


def test_class():
    my_class = CClass(
        name="my_class",
        members=[
            CClass.Constructor(arguments=[CFunction.Argument('arg', Cuint32)], access=CClass.Access.public),
            CClass.Method('my_method', arguments=[CFunction.Argument('hello', Cuint8)], access=CClass.Access.protected),
            CClass.Attribute('u8My_attr', Cuint8, initial_value=3, access=CClass.Access.private)
        ]
    )

    print(my_class.declaration())

    print(my_class.definition())

    for definition in my_class.all_members_definition():
        print(definition)


if __name__ == "__main__":
    test_class()
