from ccg import *

my_class = CClass(
    name="my_class",
    members=[
        CClass.Constructor(arguments=[CFunction.Argument('arg', Cuint32)], access=CClass.Access.public),
        CClass.Method('my_method', arguments=[CFunction.Argument('hello', Cuint8)], access=CClass.Access.protected,
                      static=True),
        CClass.Attribute('u8My_attr', Cuint8, initial_value=3, access=CClass.Access.private, static=True,
                         constexpr=True)
    ]
)

print("### Declaration")
print(my_class.declaration())

print("### Definition")
print(my_class.definition())

print("### Definition of all members")
for definition in my_class.all_members_definition():
    print(definition)
