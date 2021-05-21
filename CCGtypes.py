class GenericType:
    typename: str

    def declaration(self, *args, **kwargs):
        raise NotImplementedError("Types should implement a declaration method")

    def typedef(self, *args, **kwargs):
        raise NotImplementedError("Types should implement a typedef method")


class BasicType(GenericType):

    def declaration(self, name, semicolon=True):
        return f"{self.typename} {name}{';' if semicolon else ''}"

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


class Float(BasicType):
    typename = "float"


class Double(BasicType):
    typename = "double"


class Array(GenericType):

    def __init__(self, type, length):
        self.type = type
        self.length = length

    type = None
    length: int

    def declaration(self, name, semicolon=True):
        return f"{self.type.typename} {name}[{self.length}]{';' if semicolon else ''}"


if __name__ == "__main__":
    int8 = Int8()
    print(int8.declaration("hello"))

    print(int8.typedef('mycustomint'))

    array = Array(type=int8, length=10)
    print(array.declaration("asdf"))
