from ccg import CNamespace, CFunction
from common_style import style


def test_namespace():
    ns1 = CNamespace('ns1')
    ns2 = CNamespace('ns2', in_space=ns1)

    # Declare that function is on this namespace
    fun = CFunction(name='my_fun', in_space=ns2)

    # When doing the definition, typically is done indicating namespace inline
    print(fun.definition(style=style))

    # On the declaration it can have the same format
    print(fun.declaration(style=style))
    
    # But typically the namespace is indicated with a namespace section,
    # So we can omit inline namespace by saying that we are on a namespace
    print(fun.declaration(from_space=ns1, style=style))
    print(fun.declaration(from_space=ns2, style=style))


if __name__ == "__main__":
    test_namespace()
