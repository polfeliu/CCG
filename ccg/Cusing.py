from typing import TYPE_CHECKING

from .Cfunction import CFunction
from .Ctypes import CGenericItem
from .style import default_style

if TYPE_CHECKING:
    from .style import Style
    from .Cnamespace import CSpace


class CUsing:

    def __init__(self, item: CGenericItem):  # TODO or generic type??
        self.item = item

    def declaration(self, style: 'Style' = default_style, semicolon: bool = False, from_space: 'CSpace' = None) -> str:
        if isinstance(self.item, CFunction):
            return f"using {self.item.declaration(without_arguments=True, style=style, semicolon=semicolon, from_space=from_space)}"
        else:
            return f"using {self.item.declaration(style=style, semicolon=semicolon, from_space=from_space)}"

# TODO Move to namespace
