from typing import TYPE_CHECKING

from .style import default_style
from .variable import CVariable

if TYPE_CHECKING:
    from .style import Style


class CArray(CVariable):

    def __init__(self, name, type, length, inplace_declaration=False):
        super().__init__(name, type, inplace_declaration=inplace_declaration)
        self.length = length

    length: int

    def declaration(self, semicolon=True, style: 'Style' = default_style):
        self.style_checks(style)

        if self.inplace_declaration:
            return f"{self.type.declaration(semicolon=False, style=style)} " \
                   f"{self.name}[{self.length}]" \
                   f"{';' if semicolon else ''}"
        else:
            return f"{self.type.type_name} " \
                   f"{self.name}[{self.length}]" \
                   f"{';' if semicolon else ''}"
