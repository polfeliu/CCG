from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .types import GenericType
    from .style import Style


class HungarianNotationError(Exception):
    pass


class Variable:

    def __init__(self, name: str, type: 'GenericType', inplace_declaration=False):
        self.type = type
        self.name = name
        if hasattr(type, "declaration"):
            self.inplace_declaration = inplace_declaration
        else:
            self.inplace_declaration = False

    def check_hungarian(self):
        if not self.name.startswith(self.type.hungarian_prefix):
            raise HungarianNotationError(
                f"{self.name} doesn't doesn't have the hungarian prefix {self.type.hungarian_prefix}")
        else:
            start_letter = self.name[len(self.type.hungarian_prefix)]
            if not start_letter.isupper():
                raise HungarianNotationError(f"{self.name} first letter is not uppercase")

    def declaration(self, semicolon=True, style: Union['Style', None] = None):
        if style is not None:
            if style.check_hungarian:
                self.check_hungarian()

        if self.inplace_declaration:
            return f"{self.type.declaration(semicolon=False)} {self.name}{';' if semicolon else ''}"  # TODO
        else:
            return f"{self.type.type_name} {self.name}{';' if semicolon else ''}"
