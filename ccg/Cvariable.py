from typing import TYPE_CHECKING, Any, Optional

from .Ctypes import CGenericItem
from .Ctypes import HungarianNotationError
from .style import default_style

if TYPE_CHECKING:
    from .Ctypes import CGenericType
    from .style import Style
    from .Cnamespace import CSpace
    from .doc import Doc
    from .Cexpression import CExpression


def hungarize(name: str, c_type: 'CGenericType'):
    return c_type.hungarian_prefixes[0] + name[0].upper() + name[1:]


class CVariable(CGenericItem):

    def __init__(self,
                 name: str,
                 c_type: 'CGenericType',
                 initial_value: 'CExpression' = None,
                 static: bool = False,
                 const: bool = False,
                 constexpr: bool = False,
                 auto_hungarize: bool = False,
                 doc: Optional['Doc'] = None
                 ):
        if auto_hungarize:
            name = hungarize(name, c_type)

        super(CVariable, self).__init__(
            name=name,
            doc=doc
        )
        self.c_type = c_type
        self.initial_value = initial_value

        self.static = static
        self.const = const
        self.constexpr = constexpr

    def style_checks(self, style: 'Style') -> None:
        self.c_type.style_checks(style)
        if style.check_hungarian:
            if not style.check_hungarian_variable(
                    variable_name=self.name,
                    hungarian_prefixes=self.c_type.hungarian_prefixes
            ):
                raise HungarianNotationError(
                    f"{self.name} doesn't doesn't have the hungarian prefix {self.c_type.hungarian_prefixes} "
                    f"or the first letter is not uppercase")

    def declaration(self,
                    style: 'Style' = default_style,
                    semicolon: bool = True,
                    doc: bool = True,
                    from_space: 'CSpace' = None,
                    without_arguments: bool = False
                    ) -> str:
        self.style_checks(style)

        return (
            f"{self.doc_render(style) if doc else ''}"
            f"{'static ' if self.static else ''}"
            f"{'const ' if self.const else ''}"
            f"{'constexpr ' if self.constexpr else ''}"
            f"{self.c_type.declaration(style=style, semicolon=False, from_space=from_space)}"
            f" {self.name}"
            f"{' = ' + str(self.initial_value.render()) if self.initial_value is not None else ''}"
            f"{';' if semicolon else ''}"
        )

    @property
    def bit_size(self) -> int:
        if self.c_type.bit_size is None:
            raise ValueError("Cannot determine bit_size")
        return self.c_type.bit_size
