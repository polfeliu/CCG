from ccg import *


def test_namespace():
    ns1 = CNamespace('ns1')
    ns2 = CNamespace('ns2', in_space=ns1)

    # Declare that function is on this namespace
    fun = CFunction(name='my_fun', in_space=ns2)

    # When doing the definition, typically is done indicating namespace inline
    print(fun.define().render())

    # On the declaration it can have the same format
    print(fun.declare().render())
    
    # But typically the namespace is indicated with a namespace section,
    # So we can omit inline namespace by saying that we are on a namespace
    print(fun.declare(from_space=ns1).render())
    print(fun.declare(from_space=ns2).render())


if __name__ == "__main__":
    test_namespace()
