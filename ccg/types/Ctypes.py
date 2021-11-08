from abc import ABC, abstractmethod
from copy import copy
from typing import TYPE_CHECKING, List, Any, Optional

from ..Cnamespace import CSpace
from ..statements import CStatement, CDeclaration
from ..style import default_style

if TYPE_CHECKING:
    from ..style import Style
    from ..doc import Doc


class HungarianNotationError(Exception):
    pass


class CGenericItem(CSpace, ABC):

    def __init__(self,
                 name: str,
                 in_space: Optional['CSpace'] = None,
                 doc: Optional['Doc'] = None
                 ):
        super(CGenericItem, self).__init__(
            name=name,
            in_space=in_space
        )
        self.doc = doc

    def declare(self, from_space: 'CSpace' = None) -> 'CDeclaration':
        return CDeclaration(
            render_function=self.declaration,
            from_space=from_space
        )

    @abstractmethod
    def declaration(self,
                    style: 'Style' = default_style,
                    semicolon: bool = True,
                    doc: bool = True,
                    from_space: 'CSpace' = None
                    ) -> str:
        raise NotImplemented

    def doc_render(self, style: 'Style') -> str:
        if self.doc is None:
            return ""

        return self.doc.render(style, content=None)


class CItemDefinable(ABC):
    @abstractmethod
    def definition(self,
                   style: 'Style' = default_style,
                   from_space: 'CSpace' = None,
                   doc: bool = False
                   ) -> str:
        return ""

    def define(self, from_space: 'CSpace' = None) -> 'CDeclaration':
        return CDeclaration(
            render_function=self.definition,
            from_space=from_space,
        )


class CGenericType(CGenericItem):

    def __init__(self,
                 name: str,
                 bit_size: Optional[int] = None,
                 hungarian_prefixes: Optional[List[str]] = None,
                 derived_from: Optional['CGenericType'] = None,
                 in_space: Optional['CSpace'] = None,
                 doc: Optional['Doc'] = None
                 ):
        super(CGenericType, self).__init__(
            name=name,
            in_space=in_space,
            doc=doc
        )
        if hungarian_prefixes is None:
            hungarian_prefixes = ["t"]
        self.hungarian_prefixes = hungarian_prefixes
        self.derived_from = derived_from
        self._bit_size = bit_size

    @property
    def bit_size(self) -> int:
        if self._bit_size is None:
            raise ValueError("Cannot determine bit_size")
        return self._bit_size

    def declaration(self,
                    style: 'Style' = default_style,
                    semicolon: bool = True,
                    doc: bool = True,
                    from_space: 'CSpace' = None,
                    without_arguments: bool = False,
                    for_variable: bool = False
                    ) -> str:
        """Type declaration

        Args:
            style: generating style
            semicolon: include semicolon in declaration
            doc: include documentation
            from_space: relative to space
            without_arguments: include arguments if any
            for_variable: if the declaration is for a variable

        Returns:

        """
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

    def typedef_render(self,
                       style: 'Style' = default_style,
                       from_space: 'CSpace' = None,
                       doc: Optional['Doc'] = None
                       ) -> str:
        if self.derived_from is None:
            raise TypeError(f"Cannot typedef type {self.name} that is not derived from another type")
        return (
            f"{doc.render(style) if doc is not None else ''}"
            f"typedef "
            f"{self.derived_from.declaration(style=style, semicolon=False, doc=False, from_space=from_space)} "
            f"{self.name};"
        )

    def typedef(self, doc: Optional['Doc'] = None) -> CStatement:
        return CStatement(
            render_function=self.typedef_render,
            doc=doc
        )


class CStdType(CGenericType):

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
