from ccg import *

var = CVariable(
    c_type=Cint8,
    name="i8Mycustomint",
    initial_value=4
)
print(var.declaration())
