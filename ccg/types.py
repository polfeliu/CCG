from abc import ABC, abstractmethod


class GenericType(ABC):
    typename: str

    @abstractmethod
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




