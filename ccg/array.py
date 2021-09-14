from typing import TYPE_CHECKING

from .style import default_style
from .variable import CVariable

if TYPE_CHECKING:
    from .style import Style


class CArray(CVariable):

    def __init__(self, name, type, length):
        super().__init__(name, type)
        self.length = length

    length: int

    def declaration(self, semicolon=True, style: 'Style' = default_style):
        self.style_checks(style)

        return f"{self.type.declaration(semicolon=False, style=style)} " \
               f"{self.name}[{self.length}]" \
               f"{';' if semicolon else ''}"
