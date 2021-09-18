from typing import TYPE_CHECKING

from .style import default_style
from .Cvariable import CVariable

if TYPE_CHECKING:
    from .style import Style
    from .Ctypes import CGenericType
    from .Cnamespace import CSpace


class CArray(CVariable):

    def __init__(self, name: str, c_type: 'CGenericType', length: int):
        super().__init__(name, c_type)
        self.length = length

    def declaration(self, semicolon=True, style: 'Style' = default_style, from_space: 'CSpace' = None) -> str:
        self.style_checks(style)

        return f"{self.c_type.declaration(semicolon=False, style=style, from_space=from_space)} " \
               f"{self.name}[{self.length}]" \
               f"{';' if semicolon else ''}"
