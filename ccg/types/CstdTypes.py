from typing import TYPE_CHECKING, List, Any, Optional

from .Ctypes import CGenericType

if TYPE_CHECKING:
    from ..style import Style
    from ..doc import Doc


class CStdType(CGenericType):
    """Standard Type"""

    def literal_suffix(self, style: 'Style'):
        if self is Cfloat:
            return style.literal_float_token
        elif self is Cdouble:
            return style.literal_double_token
        elif self is Cbool:
            return ""
        else:
            raise NotImplemented


class CIntegerType(CStdType):
    """Integer Type"""

    def __init__(self,
                 name: str,
                 hungarian_prefixes: Optional[List[str]],
                 bits: int,
                 is_signed: bool
                 ):
        super(CIntegerType, self).__init__(
            name=name,
            hungarian_prefixes=hungarian_prefixes,
            bit_size=bits
        )
        self.is_signed = is_signed
        if self.is_signed:
            self.minimum = -2 ** (bits - 1)
            self.maximum = 2 ** (bits - 1) - 1
        else:
            self.minimum = 0
            self.maximum = 2 ** bits - 1

    def literal_suffix(self, style: 'Style'):
        suffix = ""

        if not self.is_signed:
            suffix += style.literal_unsigned_token

        if self.bit_size in [8, 16]:
            pass
        elif self.bit_size == 32:
            suffix += style.literal_long_token
        elif self.bit_size == 64:
            suffix += style.literal_long_token * 2
        else:
            raise TypeError

        return suffix

    def check_value(self, value: Any) -> bool:
        return value in range(self.minimum, self.maximum + 1)


Cint8 = CIntegerType(
    name="int8_t",
    hungarian_prefixes=["i8"],
    bits=8,
    is_signed=True
)
"""uint8_t"""

Cuint8 = CIntegerType(
    name="uint8_t",
    hungarian_prefixes=["u8"],
    bits=8,
    is_signed=False
)

Cint16 = CIntegerType(
    name="int16_t",
    hungarian_prefixes=["i16"],
    bits=16,
    is_signed=True
)

Cuint16 = CIntegerType(
    name="uint16_t",
    hungarian_prefixes=["u16"],
    bits=16,
    is_signed=False
)

Cint32 = CIntegerType(
    name="int32_t",
    hungarian_prefixes=["i32"],
    bits=32,
    is_signed=True
)

Cuint32 = CIntegerType(
    name="uint32_t",
    hungarian_prefixes=["u32"],
    bits=32,
    is_signed=False
)

Cint64 = CIntegerType(
    name="int8_t",
    hungarian_prefixes=["i64"],
    bits=64,
    is_signed=True
)

Cuint64 = CIntegerType(
    name="uint64_t",
    hungarian_prefixes=["u64"],
    bits=64,
    is_signed=False
)

Cfloat = CStdType(
    name="float",
    hungarian_prefixes=["f"],
    bit_size=32
)

Cdouble = CStdType(
    name="double",
    hungarian_prefixes=["db"],
    bit_size=64
)

Cbool = CStdType(
    name="bool",
    hungarian_prefixes=["b", "is"],
)

CVoidType = CGenericType(
    name='void'
)

CNoType = CGenericType(
    name=''
)


class StdTypes:
    Cint8 = Cint8
    Cuint8 = Cuint8
    Cint16 = Cint16
    Cuint16 = Cuint16
    Cint32 = Cint32
    Cuint32 = Cuint32
    Cint64 = Cint64
    Cuint64 = Cuint64
    Cfloat = Cfloat
    Cdouble = Cdouble
    Cbool = Cbool
