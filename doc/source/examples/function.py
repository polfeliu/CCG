from ccg import *

f = CFunction(
    name="examplefun",
    return_type=Cuint32,
    arguments=[
        CFunction.Argument(name="first", c_type=Cuint32),
        CFunction.Argument(name="second", c_type=Cdouble, default=2)
    ],
    static=True
)

print("### Declaration")
print(f.declaration())

print("### Definition")
print(f.definition())
