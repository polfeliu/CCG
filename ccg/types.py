from abc import ABC, abstractmethod
from typing import Union, TYPE_CHECKING

if TYPE_CHECKING:
    from .style import Style


class HungarianNotationError(Exception):
    pass


class CGenericType(ABC):
    type_name: str
    hungarian_prefix = "t"

    @abstractmethod
    def typedef(self, *args, **kwargs):
        raise NotImplementedError("Types should implement a typedef method")

    def declaration(self, semicolon=True, style: Union['Style', None] = None):
        raise NotImplementedError(f"Only Structs and Unions types can be declared, not {self.type_name}")

    def check_hungarian(self):
        if self not in std_types:
            if not self.type_name.startswith('T'):
                raise HungarianNotationError(f"Generic Type ({self.type_name}) Doesn't start with T hungarian style prefix")
            else:
                start_letter = self.type_name[len(self.hungarian_prefix)]
                if not start_letter.isupper():
                    raise HungarianNotationError(f"{self.type_name} first letter is not uppercase")


class CBasicType(CGenericType):

    def __init__(self, type_name, hungarian_prefix=None):
        self.type_name = type_name

        if hungarian_prefix is not None:
            self.hungarian_prefix = hungarian_prefix

    def typedef(self, name, style: Union['Style', None] = None):
        return f"typedef {self.type_name} {name};"


int8 = CBasicType(
    type_name="int8_t",
    hungarian_prefix="i8"
)

uint8 = CBasicType(
    type_name="uint8_t",
    hungarian_prefix="u8"
)

int16 = CBasicType(
    type_name="int16_t",
    hungarian_prefix="i16"
)

uint16 = CBasicType(
    type_name="uint16_t",
    hungarian_prefix="u16"
)

int32 = CBasicType(
    type_name="int32_t",
    hungarian_prefix="i32"
)

uint32 = CBasicType(
    type_name="uint32_t",
    hungarian_prefix="u32"
)

int64 = CBasicType(
    type_name="int8_t",
    hungarian_prefix="i64"
)

uint64 = CBasicType(
    type_name="uint64_t",
    hungarian_prefix="u64"
)

float = CBasicType(
    type_name="float",
    hungarian_prefix="f"
)

double = CBasicType(
    type_name="double",
    hungarian_prefix="db"
)

bool = CBasicType(
    type_name="bool",
    hungarian_prefix=["b", "is"]
)

std_types = [
    int8,
    uint8,
    int16,
    uint16,
    int32,
    uint32,
    int64,
    uint64,
    float,
    double,
    bool
]
