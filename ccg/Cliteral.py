from typing import TYPE_CHECKING, Union, Optional
from enum import Enum
from .Cexpression import CExpression
from .style import default_style
from .Ctypes import CIntegerType

if TYPE_CHECKING:
    from .style import Style


class CLiteral(CExpression):
    class Format(Enum):
        decimal = 10
        octal = 8
        hexadecimal = 16
        binary = 2

    def __init__(self,
                 literal: Union[int, float],
                 c_type: Union[CIntegerType, None] = None,
                 literal_format: Optional[Format] = None
                 ):
        self.literal = literal
        self.c_type = c_type
        self.literal_format = literal_format

    def format_prefix(self):
        if self.literal_format == self.Format.decimal:
            return ""
        elif self.literal_format == self.Format.octal:
            return "0"
        elif self.literal_format == self.Format.hexadecimal:
            return "0x"
        elif self.literal_format == self.Format.binary:
            return "0b"
        else:
            raise NotImplemented

    def format_literal(self) -> str:
        if isinstance(self.literal, int):
            if self.literal_format == self.Format.decimal:
                return f"{self.literal:d}"
            elif self.literal_format == self.Format.octal:
                return f"{self.literal:o}"
            elif self.literal_format == self.Format.hexadecimal:
                return f"{self.literal:x}"
            elif self.literal_format == self.Format.binary:
                return f"{self.literal:b}"
            else:
                raise NotImplemented
        else:
            raise NotImplemented

    def render(self, style: 'Style' = default_style) -> str:
        return (
            f"{self.format_prefix()}"
            f"{self.format_literal()}"
            f"{self.c_type.literal_suffix(style) if self.c_type is not None else ''}"
        )
