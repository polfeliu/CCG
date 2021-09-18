from typing import TYPE_CHECKING, Union, List, Any
from copy import copy

from .style import default_style

if TYPE_CHECKING:
    from .style import Style


class HungarianNotationError(Exception):
    pass


class CGenericType:

    def __init__(self,
                 name: str,
                 hungarian_prefixes: Union[List[str], str] = "t",
                 derived_from: Union['CGenericType', None] = None):
        self.name = name
        self.hungarian_prefixes = hungarian_prefixes
        if not isinstance(self.hungarian_prefixes, list):
            self.hungarian_prefixes = [self.hungarian_prefixes]
        self.derived_from = derived_from

    def declaration(self, semicolon: bool = False, style: 'Style' = default_style) -> str:
        return self.name + (';' if semicolon else '')

    def check_value(self, value: Any) -> bool:
        """Checks that a value is correct for the type

        Args:
            value: value to check

        Returns:
            boolean indicating if value fits type (True) or not
        """
        raise NotImplementedError

    def style_checks(self, style: 'Style') -> None:
        # hungarian
        if self not in std_types:
            if not self.name.startswith('T'):
                raise HungarianNotationError(
                    f"Generic Type ({self.name}) Doesn't start with T hungarian style prefix")
            else:
                start_letter = self.name[1]
                if not start_letter.isupper():
                    raise HungarianNotationError(f"{self.name} first letter is not uppercase")

    def type(self, name: str) -> 'CGenericType':
        new_type = copy(self)
        new_type.name = name
        new_type.derived_from = self
        new_type.hungarian_prefixes = ["t"]

        return new_type

    def typedef(self, style: 'Style' = default_style):
        return f"typedef {self.derived_from.declaration(semicolon=False, style=style)} {self.name};"


class CIntegerType(CGenericType):

    def __init__(self, name: str, hungarian_prefixes: Union[List[str], str], bits: int, isSigned: bool):
        super(CIntegerType, self).__init__(
            name=name,
            hungarian_prefixes=hungarian_prefixes
        )
        if isSigned:
            self.minimum = -2 ** (bits - 1)
            self.maximum = 2 ** (bits - 1) - 1
        else:
            self.minimum = 0
            self.maximum = 2 ** (bits) - 1

    def check_value(self, value: Any) -> bool:
        return value in range(self.minimum, self.maximum + 1)


Cint8 = CIntegerType(
    name="int8_t",
    hungarian_prefixes="i8",
    bits=8,
    isSigned=True
)

Cuint8 = CIntegerType(
    name="uint8_t",
    hungarian_prefixes="u8",
    bits=8,
    isSigned=False
)

Cint16 = CIntegerType(
    name="int16_t",
    hungarian_prefixes="i16",
    bits=16,
    isSigned=True
)

Cuint16 = CIntegerType(
    name="uint16_t",
    hungarian_prefixes="u16",
    bits=16,
    isSigned=False
)

Cint32 = CIntegerType(
    name="int32_t",
    hungarian_prefixes="i32",
    bits=32,
    isSigned=True
)

Cuint32 = CIntegerType(
    name="uint32_t",
    hungarian_prefixes="u32",
    bits=32,
    isSigned=False
)

Cint64 = CIntegerType(
    name="int8_t",
    hungarian_prefixes="i64",
    bits=64,
    isSigned=True
)

Cuint64 = CIntegerType(
    name="uint64_t",
    hungarian_prefixes="u64",
    bits=64,
    isSigned=False
)

Cfloat = CGenericType(
    name="float",
    hungarian_prefixes="f",
)

Cdouble = CGenericType(
    name="double",
    hungarian_prefixes="db",
)

Cbool = CGenericType(
    name="bool",
    hungarian_prefixes=["b", "is"]
)

std_types = [
    Cint8,
    Cuint8,
    Cint16,
    Cuint16,
    Cint32,
    Cuint32,
    Cint64,
    Cuint64,
    Cfloat,
    Cdouble,
    Cbool
]
