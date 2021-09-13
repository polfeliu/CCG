from abc import ABC, abstractmethod
from typing import Union, TYPE_CHECKING

if TYPE_CHECKING:
    from .style import Style


class GenericType(ABC):
    type_name: str
    hungarian_prefix = "t"

    @abstractmethod
    def typedef(self, *args, **kwargs):
        raise NotImplementedError("Types should implement a typedef method")

    def declaration(self, semicolon=True):
        raise NotImplementedError(f"Only Structs and Unions types can be declared, not {self.type_name}")


class BasicType(GenericType):

    def __init__(self, type_name, hungarian_prefix):
        self.type_name = type_name
        self.hungarian_prefix = hungarian_prefix

    def typedef(self, name, style: Union['Style', None] = None):
        return f"typedef {self.type_name} {name};"


Int8 = BasicType(
    type_name="int8_t",
    hungarian_prefix="i8"
)

UInt8 = BasicType(
    type_name="uint8_t",
    hungarian_prefix="u8"
)

Int16 = BasicType(
    type_name="int16_t",
    hungarian_prefix="i16"
)

UInt16 = BasicType(
    type_name="uint16_t",
    hungarian_prefix="u16"
)

Int32 = BasicType(
    type_name="int32_t",
    hungarian_prefix="i32"
)

UInt32 = BasicType(
    type_name="uint32_t",
    hungarian_prefix="u32"
)

Int64 = BasicType(
    type_name="int8_t",
    hungarian_prefix="i8"
)

UInt64 = BasicType(
    type_name="uint64_t",
    hungarian_prefix="u64"
)

Float = BasicType(
    type_name="float",
    hungarian_prefix="f"
)

Double = BasicType(
    type_name="double",
    hungarian_prefix="db"
)
