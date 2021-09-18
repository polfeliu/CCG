from typing import TYPE_CHECKING, Union, List
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


class CBasicType(CGenericType):

    def __init__(self, name: str, hungarian_prefixes: Union[List[str], str]):
        super(CBasicType, self).__init__(
            name=name,
            hungarian_prefixes=hungarian_prefixes
        )


Cint8 = CBasicType(
    name="int8_t",
    hungarian_prefixes="i8"
)

Cuint8 = CBasicType(
    name="uint8_t",
    hungarian_prefixes="u8"
)

Cint16 = CBasicType(
    name="int16_t",
    hungarian_prefixes="i16"
)

Cuint16 = CBasicType(
    name="uint16_t",
    hungarian_prefixes="u16"
)

Cint32 = CBasicType(
    name="int32_t",
    hungarian_prefixes="i32"
)

Cuint32 = CBasicType(
    name="uint32_t",
    hungarian_prefixes="u32"
)

Cint64 = CBasicType(
    name="int8_t",
    hungarian_prefixes="i64"
)

Cuint64 = CBasicType(
    name="uint64_t",
    hungarian_prefixes="u64"
)

Cfloat = CBasicType(
    name="float",
    hungarian_prefixes="f"
)

Cdouble = CBasicType(
    name="double",
    hungarian_prefixes="db"
)

Cbool = CBasicType(
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
