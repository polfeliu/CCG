from ccg import *

my_new_type = CVariable(
    c_type=CGenericType('FreeStyleType'),
    name="tMyvar",
)
# Assume the FreeStyleType is already declared
print(my_new_type.declaration())
