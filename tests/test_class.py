from ccg import CClass, CClassConstructor, CClassMethod, CClassAttribute, CFunctionArgument
from ccg.types import *
from common_style import style


def test_types():
    my_class = CClass(
        name="my_class",
        members=[
            CClassConstructor(
                arguments=[CFunctionArgument('arg', Cuint32)]
            )
        ]
    )

    print(my_class.declaration())

    print(my_class.definition())


if __name__ == "__main__":
    test_types()
