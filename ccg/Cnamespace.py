from typing import TYPE_CHECKING, List, Union

if TYPE_CHECKING:
    from .Ctypes import CGenericItem


class CSpace:

    def __init__(self, name: str, in_space: Union['CSpace', None] = None):
        self.name = name
        self.in_space = in_space

    @property
    def full_space_list(self) -> List['CSpace']:
        if self.in_space is None:
            return [self]
        else:
            return [self] + self.in_space.full_space_list

    def space_def(self, from_space: 'CSpace' = None) -> str:
        space_def = ""
        space_list = reversed(self.full_space_list[1:])
        if from_space is not None:
            # Remove redundant space
            space_set = set(space_list)
            from_space_set = set(from_space.full_space_list)
            space_set = space_set - from_space_set
            space_list = list(space_set)

        for space in space_list:
            space_def += (space.name + "::")

        return space_def


class CNamespace(CSpace):
    pass
