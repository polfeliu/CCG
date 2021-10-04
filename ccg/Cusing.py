from typing import TYPE_CHECKING

from .Ctypes import CGenericItem
from .style import default_style

if TYPE_CHECKING:
    from .style import Style
    from .Cnamespace import CSpace


class CUsing:

    def __init__(self, item: CGenericItem):
        self.item = item

    def declaration(self, style: 'Style' = default_style, from_space: 'CSpace' = None) -> str:
        return f"using {self.item.space_def(from_space)}{self.item.name};"
