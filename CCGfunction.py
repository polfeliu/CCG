from CCGtypes import GenericType

class FunctionArgument:

    def __init__(self, name, type):
        self.name = name
        self.type = type

    name: str = None
    type = None

class Function:

    def __init__(self, name, return_type, content=None):
        self.name = name
        self.return_type = return_type
        self.content = content

    name: str
    return_type = None
    content = None  # TODO Change content for list of statements or something like that

    def declaration(self):
        pass

    def prototype(self):
        pass

if __name__ == "__main__":
    from CCGtypes import Uint32
    f = Function(
        name="examplefun",
        return_type=Uint32