from ccg import *

# Static
var = CVariable(c_type=Cuint8, name="u8Var", static=True)
print(var.declaration())

# Static and const
var = CVariable(c_type=Cuint8, name="u8Var", static=True, const=True)
print(var.declaration())

# Constexpr
var = CVariable(c_type=Cuint8, name="u8Var", constexpr=True)
print(var.declaration())
