from typing import TYPE_CHECKING, Optional

from .types.Ctypes import CGenericItem
from .style import default_style

if TYPE_CHECKING:
    from .style import Style
    from .Cnamespace import CSpace
    from .doc import Doc


class CUsing(CGenericItem):

    def __init__(self,
                 item: CGenericItem,
                 in_space: Optional['CSpace'] = None,
                 doc: Optional['Doc'] = None
                 ):
        super(CUsing, self).__init__(
            name="",
            in_space=in_space,
            doc=doc
        )
        self.item = item

    def declaration(self,
                    style: 'Style' = default_style,
                    semicolon: bool = True,
                    doc: bool = True,
                    from_space: 'CSpace' = None
                    ) -> str:
        return (
            f"{self.doc_render(style) if doc else ''}"
            f"using "
            f"{self.item.space_def(from_space)}{self.item.name}"
            f"{';' if semicolon else ''}"
        )

    def doc_render(self, style: 'Style') -> str:
        if self.doc is None:
            return ""

        return self.doc.render(style, content=None)
