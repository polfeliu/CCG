# TODO typing

class CSpace:

    def __init__(self, item, in_space=None):
        self.item = item
        self.in_space = in_space

    @property
    def full_space_list(self):
        return [self]

class CNamespace(CSpace):
    pass
