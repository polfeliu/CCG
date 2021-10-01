from ccg import *

array = CArray(
    c_type=Cint8,
    name="i8Asdf",
    length=10
)
print(array.declaration())
