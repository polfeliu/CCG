from typing import TYPE_CHECKING, List, Optional

if TYPE_CHECKING:
    pass


class CSpace:

    def __init__(self, name: str, in_space: Optional['CSpace'] = None):
        self.name = name
        self.in_space = in_space

    @property
    def full_space_list(self) -> List['CSpace']:
        if self.in_space is None:
            return [self]
        else:
            return self.in_space.full_space_list + [self]

    def space_def(self, from_space: 'CSpace' = None) -> str:
        space_def = ""
        space_list = self.full_space_list
        if from_space is not None:
            # Remove redundant space
            from_space_list = from_space.full_space_list
            for space in from_space_list:
                if space == space_list[0]:
                    del space_list[0]

        del space_list[-1]
        for space in space_list:
            space_def += (space.name + "::")

        return space_def


class CNamespace(CSpace):
    pass
