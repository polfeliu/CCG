from typing import TYPE_CHECKING

from .Cvariable import CVariable
from .style import default_style

if TYPE_CHECKING:
    from .style import Style
    from .Ctypes import CGenericType
    from .Cnamespace import CSpace


class CArray(CVariable):

    def __init__(self, name: str, c_type: 'CGenericType', length: int):
        super().__init__(name, c_type)
        self.length = length

    def declaration(self, style: 'Style' = default_style, semicolon: bool = True, from_space: 'CSpace' = None) -> str:
        self.style_checks(style)

        return f"{self.c_type.declaration(semicolon=False, style=style, from_space=from_space)} " \
               f"{self.name}[{self.length}]" \
               f"{';' if semicolon else ''}"

    @property
    def hungarian_prefixes(self):
        return self.c_type.hungarian_prefixes

    @property
    def bit_size(self):
        return self.c_type.bit_size * self.length
