from typing import TYPE_CHECKING, Union, List

from .statements import CDeclarations, CDeclaration

if TYPE_CHECKING:
    pass


class File:

    def __init__(self, declarations: Union['CDeclarations', List['CDeclaration']]):
        if isinstance(declarations, CDeclaration):
            self.declarations = declarations
        else:
            self.declarations = CDeclarations(declarations)

    def generate(self, path: str):
        with open(path, "w+") as output:
            output.write(self.declarations.render())
