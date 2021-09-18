# TODO typing

class CSpace:

    def __init__(self, item, in_space=None):
        self.item = item
        self.in_space = in_space

    @property
    def full_space_list(self):
        if self.in_space is None:
            return [self]
        else:
            return [self, self.in_space.full_space_list]

    @property
    def full_space(self):
        space_def = ""
        if self.space is not None:
            for space in self.space.full_space_list:
                space_def += f"{space.item.name}::"

        return space_def


class CNamespace(CSpace):
    pass
