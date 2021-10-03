from ccg import CClass, CFunction
from ccg.Ctypes import *


def test_class():
    base_class = CClass(
        name="BaseClass",
        members=[
            CClass.Constructor(arguments=[CFunction.Argument('arg', Cuint32)], access=CClass.Access.public),
        ]
    )

    my_class = CClass(
        name="InheritedClass",
        inherit_from=CClass.Inherit(base_class, access=CClass.Access.public),
        members=[
            CClass.Using(base_class.constructor, access=CClass.Access.public),
            CClass.Method('my_method', arguments=[CFunction.Argument('hello', Cuint8)], access=CClass.Access.protected,
                          static=True),
            CClass.Attribute('u8My_attr', Cuint8, initial_value=3, access=CClass.Access.private, static=True,
                             constexpr=True),
            CClass.TypeMember(Cuint8.type('NewType'), access=CClass.Access.public),
        ]
    )

    print(my_class.declaration())

    print(my_class.definition())

    for definition in my_class.all_members_definition():
        print(definition)


if __name__ == "__main__":
    test_class()
