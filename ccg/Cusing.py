from .Ctypes import CGenericItem, CGenericType
from .style import default_style
from .Cfunction import CFunction

class CUsing:

    def __init__(self, item: CGenericItem):  # TODO or generic type??
        self.item = item

    def declaration(self, semicolon: bool = False, style: 'Style' = default_style, from_space: 'CSpace' = None) -> str:
        if isinstance(self.item, CFunction):
            return f"using {self.item.declaration(without_arguments=True)}"
        else:
            return f"using {self.item.declaration()}"

# TODO Move to namespace