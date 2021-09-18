from typing import Union, TYPE_CHECKING
from copy import copy

from .style import default_style

if TYPE_CHECKING:
    from .style import Style


class HungarianNotationError(Exception):
    pass


class CGenericType:
    type_name: str
    hungarian_prefix = "t"
    derived_from: Union['CGenericType', None] = None

    def declaration(self, semicolon: bool = False, style: 'Style' = default_style):
        return self.type_name + (';' if semicolon else '')

    def style_checks(self, style: 'Style'):
        # hungarian
        if self not in std_types:
            if not self.type_name.startswith('T'):
                raise HungarianNotationError(
                    f"Generic Type ({self.type_name}) Doesn't start with T hungarian style prefix")
            else:
                start_letter = self.type_name[1]
                if not start_letter.isupper():
                    raise HungarianNotationError(f"{self.type_name} first letter is not uppercase")

    def type(self, name: str):
        new_type = copy(self)
        new_type.type_name = name
        new_type.derived_from = self
        new_type.hungarian_prefix = CGenericType.hungarian_prefix

        return new_type

    def typedef(self, style: 'Style' = default_style):
        return f"typedef {self.derived_from.declaration(semicolon=False, style=style)} {self.type_name};"


class CBasicType(CGenericType):

    def __init__(self, type_name, hungarian_prefix=None):
        self.type_name = type_name

        if hungarian_prefix is not None:
            self.hungarian_prefix = hungarian_prefix


Cint8 = CBasicType(
    type_name="int8_t",
    hungarian_prefix="i8"
)

Cuint8 = CBasicType(
    type_name="uint8_t",
    hungarian_prefix="u8"
)

Cint16 = CBasicType(
    type_name="int16_t",
    hungarian_prefix="i16"
)

Cuint16 = CBasicType(
    type_name="uint16_t",
    hungarian_prefix="u16"
)

Cint32 = CBasicType(
    type_name="int32_t",
    hungarian_prefix="i32"
)

Cuint32 = CBasicType(
    type_name="uint32_t",
    hungarian_prefix="u32"
)

Cint64 = CBasicType(
    type_name="int8_t",
    hungarian_prefix="i64"
)

Cuint64 = CBasicType(
    type_name="uint64_t",
    hungarian_prefix="u64"
)

Cfloat = CBasicType(
    type_name="float",
    hungarian_prefix="f"
)

Cdouble = CBasicType(
    type_name="double",
    hungarian_prefix="db"
)

Cbool = CBasicType(
    type_name="bool",
    hungarian_prefix=["b", "is"]
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
