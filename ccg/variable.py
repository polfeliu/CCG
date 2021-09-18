from typing import TYPE_CHECKING

from .style import default_style
from .types import HungarianNotationError

if TYPE_CHECKING:
    from .types import CGenericType
    from .style import Style


class CVariable:

    def __init__(self, name: str, type: 'CGenericType'):
        self.type = type
        self.name = name

    def style_checks(self, style: 'Style'):
        self.type.style_checks(style)

        # hungarian
        if not style.check_hungarian_variable(
                variable_name=self.name,
                hungarian_prefixes=self.type.hungarian_prefixes
        ):
            raise HungarianNotationError(
                f"{self.name} doesn't doesn't have the hungarian prefix [{self.type.hungarian_prefixes}] "
                f"or the first letter is not uppercase")

    def declaration(self, semicolon=True, style: 'Style' = default_style):
        self.style_checks(style)

        return f"{self.type.declaration(semicolon=False, style=style)} {self.name}{';' if semicolon else ''}"  # TODO
