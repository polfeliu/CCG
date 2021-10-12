from abc import ABC, abstractmethod
from copy import copy
from typing import TYPE_CHECKING, Union, List, Any

from .Cnamespace import CSpace
from .Cstatement import CStatement
from .style import default_style

if TYPE_CHECKING:
    from .style import Style
    from .doc import Doc


class HungarianNotationError(Exception):
    pass


class CGenericItem(CSpace, ABC):

    def __init__(self, name, in_space: Union['CSpace', None] = None, doc: Union['Doc', None] = None):
        super(CGenericItem, self).__init__(
            name=name,
            in_space=in_space
        )
        self.doc = doc

    def declare(self) -> CStatement:
        return CStatement(
            render_function=self.declaration
        )

    @abstractmethod
    def declaration(self, style: 'Style' = default_style, semicolon: bool = True, from_space: 'CSpace' = None) -> str:
        raise NotImplemented


class CGenericType(CGenericItem):

    def __init__(self,
                 name: str,
                 bit_size: int = None,
                 hungarian_prefixes: Union[List[str], str] = "t",
                 derived_from: Union['CGenericType', None] = None,
                 in_space: Union['CSpace', None] = None,
                 doc: Union['Doc', None] = None
                 ):
        super(CGenericType, self).__init__(
            name=name,
            in_space=in_space,
            doc=doc
        )
        self.hungarian_prefixes = hungarian_prefixes
        if not isinstance(self.hungarian_prefixes, list):
            self.hungarian_prefixes = [self.hungarian_prefixes]
        self.derived_from = derived_from
        self.bit_size = bit_size

    def declaration(self, style: 'Style' = default_style, semicolon: bool = False, from_space: 'CSpace' = None) -> str:
        return self.name + (';' if semicolon else '')

    def check_value(self, value: Any) -> bool:
        """Checks that a value is correct for the type

        Args:
            value: value to check

        Returns:
            boolean indicating if value fits type (True) or not
        """
        return True  # Generic type accept everything. Override this method to check custom types

    def style_checks(self, style: 'Style') -> None:
        if style.check_hungarian:
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

    def typedef(self, style: 'Style' = default_style, from_space: 'CSpace' = None) -> str:
        return (f"typedef "
                f"{self.derived_from.declaration(style=style, semicolon=False, from_space=from_space)} "
                f"{self.name};")


class CIntegerType(CGenericType):

    def __init__(self, name: str, hungarian_prefixes: Union[List[str], str], bits: int, is_signed: bool):
        super(CIntegerType, self).__init__(
            name=name,
            hungarian_prefixes=hungarian_prefixes
        )
        if is_signed:
            self.minimum = -2 ** (bits - 1)
            self.maximum = 2 ** (bits - 1) - 1
        else:
            self.minimum = 0
            self.maximum = 2 ** bits - 1
        self.bit_size = bits

    def check_value(self, value: Any) -> bool:
        return value in range(self.minimum, self.maximum + 1)


Cint8 = CIntegerType(
    name="int8_t",
    hungarian_prefixes="i8",
    bits=8,
    is_signed=True
)

Cuint8 = CIntegerType(
    name="uint8_t",
    hungarian_prefixes="u8",
    bits=8,
    is_signed=False
)

Cint16 = CIntegerType(
    name="int16_t",
    hungarian_prefixes="i16",
    bits=16,
    is_signed=True
)

Cuint16 = CIntegerType(
    name="uint16_t",
    hungarian_prefixes="u16",
    bits=16,
    is_signed=False
)

Cint32 = CIntegerType(
    name="int32_t",
    hungarian_prefixes="i32",
    bits=32,
    is_signed=True
)

Cuint32 = CIntegerType(
    name="uint32_t",
    hungarian_prefixes="u32",
    bits=32,
    is_signed=False
)

Cint64 = CIntegerType(
    name="int8_t",
    hungarian_prefixes="i64",
    bits=64,
    is_signed=True
)

Cuint64 = CIntegerType(
    name="uint64_t",
    hungarian_prefixes="u64",
    bits=64,
    is_signed=False
)

Cfloat = CGenericType(
    name="float",
    hungarian_prefixes="f",
    bit_size=32
)

Cdouble = CGenericType(
    name="double",
    hungarian_prefixes="db",
    bit_size=64
)

Cbool = CGenericType(
    name="bool",
    hungarian_prefixes=["b", "is"],
)

CVoidType = CGenericType(
    name='void'
)

CNoType = CGenericType(
    name=''
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
