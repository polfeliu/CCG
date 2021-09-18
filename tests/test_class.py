from ccg import CClass, CClassConstructor, CClassMethod, CClassAttribute, CFunctionArgument, CClassAccess
from ccg.types import *
from common_style import style


def test_types():
    my_class = CClass(
        name="my_class",
        members=[
            CClassConstructor(arguments=[CFunctionArgument('arg', Cuint32)], access=CClassAccess.public),
            CClassMethod('my_method', arguments=[CFunctionArgument('hello', Cuint8)], access=CClassAccess.protected),
            CClassAttribute('u8My_attr', Cuint8, initial_value=3, access=CClassAccess.private)
        ]
    )

    print(my_class.declaration())

    print(my_class.definition())

    for definition in my_class.all_members_definition():
        print(definition)


if __name__ == "__main__":
    test_types()
