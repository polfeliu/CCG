from typing import TYPE_CHECKING

from .style import default_style
from .types import HungarianNotationError

if TYPE_CHECKING:
    from .types import CGenericType
    from .style import Style


class CVariable:

    def __init__(self, name: str, type: 'CGenericType', inplace_declaration=False):
        self.type = type
        self.name = name
        if hasattr(type, "declaration"):
            self.inplace_declaration = inplace_declaration
        else:
            self.inplace_declaration = False

    def style_checks(self, style: 'Style'):
        self.type.style_checks(style)

        # hungarian
        if not self.name.startswith(self.type.hungarian_prefix):
            raise HungarianNotationError(
                f"{self.name} doesn't doesn't have the hungarian prefix {self.type.hungarian_prefix}")
        else:
            start_letter = self.name[len(self.type.hungarian_prefix)]
            if not start_letter.isupper():
                raise HungarianNotationError(f"{self.name} first letter is not uppercase")

    def declaration(self, semicolon=True, style: 'Style' = default_style):
        self.style_checks(style)

        if self.inplace_declaration:
            return f"{self.type.declaration(semicolon=False, style=style)} {self.name}{';' if semicolon else ''}"  # TODO
        else:
            return f"{self.type.type_name} {self.name}{';' if semicolon else ''}"
