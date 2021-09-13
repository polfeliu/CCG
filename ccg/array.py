from .variable import Variable


class Array(Variable):

    def __init__(self, name, type, length, inplace_declaration=False):
        super().__init__(name, type, inplace_declaration=inplace_declaration)
        self.length = length

    length: int

    def declaration(self, semicolon=True):
        if self.inplace_declaration:
            return f"{self.type.declaration(semicolon=False)} {self.name}[{self.length}]{';' if semicolon else ''}"
        else:
            return f"{self.type.typename} {self.name}[{self.length}]{';' if semicolon else ''}"
