from .variable import CVariable

from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .style import Style


class CArray(CVariable):

    def __init__(self, name, type, length, inplace_declaration=False):
        super().__init__(name, type, inplace_declaration=inplace_declaration)
        self.length = length

        # TODO hungarian

    length: int

    def declaration(self, semicolon=True, style: Union['Style', None] = None):
        if self.inplace_declaration:
            return f"{self.type.declaration(semicolon=False, style=style)} {self.name}[{self.length}]{';' if semicolon else ''}"  # TODO
        else:
            return f"{self.type.type_name} {self.name}[{self.length}]{';' if semicolon else ''}"
