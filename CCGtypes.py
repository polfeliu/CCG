class GenericType:
    typename: str

    def typedef(self, *args, **kwargs):
        raise NotImplementedError("Types should implement a typedef method")


class BasicType(GenericType):

    def typedef(self, name):
        return f"typedef {self.typename} {name};"


class Int8(BasicType):
    typename = "int8_t"


class Uint8(BasicType):
    typename = "uint8_t"


class Int16(BasicType):
    typename = "int16_t"


class Uint16(BasicType):
    typename = "uint16_t"


class Int32(BasicType):
    typename = "int32_t"


class Uint32(BasicType):
    typename = "uint32_t"


class Int64(BasicType):
    typename = "int64_t"


class Uint64(BasicType):
    typename = "uint64_t"


class Float(BasicType):
    typename = "float"


class Double(BasicType):
    typename = "double"

from CCGstruct import Struct
from CCGunion import Union

class Variable():

    def __init__(self, name, type, inplace_declaration = False):
        self.type = type
        self.name = name
        if hasattr(type, "declaration"):
            self.inplace_declaration = inplace_declaration
        else:
            self.inplace_declaration = False

    type = None
    name: str = None

    def declaration(self, semicolon=True):
        if self.inplace_declaration:
            return f"{self.type.declaration(semicolon=False)} {self.name}{';' if semicolon else ''}"
        else:
            return f"{self.type.typename} {self.name}{';' if semicolon else ''}"

class Array(Variable):

    def __init__(self, name, type, length, inplace_declaration = False):
        super().__init__(name, type, inplace_declaration= inplace_declaration)
        self.length = length

    length: int

    def declaration(self, semicolon=True):
        if self.inplace_declaration:
            return f"{self.type.declaration(semicolon=False)} {self.name}[{self.length}]{';' if semicolon else ''}"
        else:
            return f"{self.type.typename} {self.name}[{self.length}]{';' if semicolon else ''}"

if __name__ == "__main__":
    var = Variable(
        type=Int8,
        name="mycustomint"
    )
    print(var.declaration())

    print(Int8().typedef('mycustomtype'))

    array = Array(
        type=Int8,
        name="asdf",
        length=10
    )

    print(array.declaration())
