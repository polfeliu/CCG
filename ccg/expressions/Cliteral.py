from enum import Enum
from typing import TYPE_CHECKING, Union, Optional

from .Cexpression import CExpression
from ..style import default_style
from ..types.CstdTypes import CIntegerType

if TYPE_CHECKING:
    from ..style import Style


class CLiteral(CExpression):
    """Literal Value"""

    class Format(Enum):
        """Formatting Choice"""
        decimal = 10
        octal = 8
        hexadecimal = 16
        binary = 2
        float_decimals = -1
        float_scientific = -2
        boolean = -10

    def __init__(self,
                 literal: Union[int, float, bool],
                 c_type: Union[CIntegerType, None] = None,
                 literal_format: Optional[Format] = None
                 ):
        self.literal = literal
        self.c_type = c_type
        if literal_format is not None:
            self.literal_format = literal_format
        else:
            if isinstance(literal, bool):
                self.literal_format = self.Format.boolean
            elif isinstance(literal, int):
                self.literal_format = self.Format.decimal
            elif isinstance(literal, float):
                self.literal_format = self.Format.float_decimals
            else:
                raise TypeError

        if isinstance(literal, bool):
            if self.literal_format not in [self.Format.boolean]:
                raise TypeError(f"Cannot format bool with {self.literal_format}")

        elif isinstance(literal, int):
            if self.literal_format not in [self.Format.decimal, self.Format.octal, self.Format.hexadecimal,
                                           self.Format.binary]:
                if self.literal_format in [self.Format.float_decimals, self.Format.float_scientific]:
                    self.literal = float(self.literal)
                else:
                    raise TypeError(f"Cannot format integer with {self.literal_format}")

        elif isinstance(literal, float):
            if self.literal_format not in [self.Format.float_decimals, self.Format.float_scientific]:
                raise TypeError(f"Cannot format float with {self.literal_format}")
        else:
            raise TypeError

    def format_prefix(self):
        """Prefix of the literal according to the format"""
        if self.literal_format == self.Format.decimal:
            return ""
        elif self.literal_format == self.Format.octal:
            return "0"
        elif self.literal_format == self.Format.hexadecimal:
            return "0x"
        elif self.literal_format == self.Format.binary:
            return "0b"
        elif self.literal_format == self.Format.float_decimals:
            return ""
        elif self.literal_format == self.Format.float_scientific:
            return ""
        elif self.literal_format == self.Format.boolean:
            return ""
        else:
            raise NotImplemented

    def format_literal(self, style: 'Style') -> str:
        """Render the literal with the format selected.

        Does not include prefix or suffix
        """
        if isinstance(self.literal, bool):
            if self.literal_format == self.Format.boolean:
                if self.literal:
                    return style.literal_boolean_true_token
                else:
                    return style.literal_boolean_false_token
            else:
                raise NotImplemented

        elif isinstance(self.literal, int):
            if self.literal_format == self.Format.decimal:
                return f"{self.literal:d}"
            elif self.literal_format == self.Format.octal:
                return f"{self.literal:o}"
            elif self.literal_format == self.Format.hexadecimal:
                if style.literal_hexadecimal_uppercase:
                    return f"{self.literal:X}"
                else:
                    return f"{self.literal:x}"
            elif self.literal_format == self.Format.binary:
                return f"{self.literal:b}"
            else:
                raise NotImplemented
        elif isinstance(self.literal, float):
            if self.literal_format == self.Format.float_decimals:
                return str(float(f"{self.literal:g}"))
            elif self.literal_format == self.Format.float_scientific:
                return f"{self.literal:e}"
            else:
                raise NotImplemented
        else:
            raise NotImplemented

    def render(self, style: 'Style' = default_style) -> str:
        return (
            f"{self.format_prefix()}"
            f"{self.format_literal(style)}"
            f"{self.c_type.literal_suffix(style) if self.c_type is not None else ''}"
        )
