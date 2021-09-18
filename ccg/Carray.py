from typing import TYPE_CHECKING

from .style import default_style
from .Cvariable import CVariable

if TYPE_CHECKING:
    from .style import Style
    from .Ctypes import CGenericType


class CArray(CVariable):

    def __init__(self, name: str, type: 'CGenericType', length: int):
        super().__init__(name, type)
        self.length = length

    def declaration(self, semicolon=True, style: 'Style' = default_style) -> str:
        self.style_checks(style)

        return f"{self.type.declaration(semicolon=False, style=style)} " \
               f"{self.name}[{self.length}]" \
               f"{';' if semicolon else ''}"
