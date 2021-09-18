from typing import TYPE_CHECKING, Any

from .style import default_style
from .Ctypes import HungarianNotationError
from .Ctypes import CGenericItem

if TYPE_CHECKING:
    from .Ctypes import CGenericType
    from .style import Style
    from .Cnamespace import CSpace


class CVariable(CGenericItem):

    def __init__(self, name: str, c_type: 'CGenericType', initial_value: Any = None):
        super(CVariable, self).__init__(
            name=name
        )
        self.c_type = c_type
        self._initial_value = initial_value
        if initial_value is not None:
            if self.c_type.check_value(self._initial_value) is not True:
                raise ValueError(f"Initial value [{initial_value}] does not fit type [{self.c_type.name}]")

    def style_checks(self, style: 'Style'):
        self.c_type.style_checks(style)

        # hungarian
        if not style.check_hungarian_variable(
                variable_name=self.name,
                hungarian_prefixes=self.c_type.hungarian_prefixes
        ):
            raise HungarianNotationError(
                f"{self.name} doesn't doesn't have the hungarian prefix {self.c_type.hungarian_prefixes} "
                f"or the first letter is not uppercase")

    def declaration(self, semicolon=True, style: 'Style' = default_style, from_space: 'CSpace' = None):
        self.style_checks(style)

        return (f"{self.c_type.declaration(semicolon=False, style=style, from_space=from_space)}"
                f" {self.name}"
                f"{' = ' + str(self._initial_value) if self._initial_value is not None else ''}"
                f"{';' if semicolon else ''}"
                )
