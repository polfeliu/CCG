class GenericType:
    typename: str


class Int8(GenericType):

    typename = "int8"

    def declaration(self, name, semicolon=True):
        return f"{self.typename} {name}{';' if semicolon else ''}"


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

    array = Array(type=int8, length=10)
    print(int8.declaration("asdf"))