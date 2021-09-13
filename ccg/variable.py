class Variable():

    def __init__(self, name, type, inplace_declaration=False):
        self.type = type
        self.name = name
        if hasattr(type, "declaration"):
            self.inplace_declaration = inplace_declaration
        else:
            self.inplace_declaration = False

    type = None
    name: str = None

    def declaration(self, semicolon=True):
        if self.inplace_declaration:
            return f"{self.type.declaration(semicolon=False)} {self.name}{';' if semicolon else ''}"
        else:
            return f"{self.type.typename} {self.name}{';' if semicolon else ''}"
