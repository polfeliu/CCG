from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from .Ctypes import CGenericItem


class CSpace:

    def __init__(self, item: 'CGenericItem', in_space: 'CSpace' = None):
        self.item = item
        self.in_space = in_space

    @property
    def full_space_list(self) -> List['CSpace']:
        if self.in_space is None:
            return [self]
        else:
            return [self] + self.in_space.full_space_list

    @property
    def full_space(self) -> str:
        space_def = ""
        for space in reversed(self.full_space_list[1:]):
            space_def += (space.item.name + "::")

        return space_def


class CNamespace(CSpace):
    pass
