from typing import TYPE_CHECKING, Union, List, Callable

from .statements import CDeclarations, CDeclaration, CStatement
from .style import default_style

from os.path import isfile
import re

if TYPE_CHECKING:
    from .style import Style

UserCodeCallback = Callable[['Style', str], str]


class File:

    def __init__(self, declarations: Union['CDeclarations', List['CDeclaration']], style: 'Style' = default_style):
        if isinstance(declarations, CDeclaration):
            self.declarations = declarations
        else:
            self.declarations = CDeclarations(declarations)
        self.style = style

    def generate(self, path: str):
        generated = self.declarations.render()

        # self._analyze_code_sections(generated)

        if isfile(path):
            # Scan user code sections
            with open(path, "r") as current:
                current_content = current.read()
                self._analyze_code_sections(current_content)

        """with open(path, "w+") as output:
            output.write(generated)"""

    def _analyze_code_sections(self, content: str) -> dict:
        any_identifier = r'(.*)'
        pattern = (
            rf"{self.style.user_code_begin_pattern(any_identifier)}"
            rf"(.|\n|\r|\t)*?"  # Any content between
            rf"{self.style.user_code_end_pattern(any_identifier)}"
        )

        # print(pattern)

        for a in re.finditer(pattern, content):
            print(a.group())
        print("####")

        return {}


class UserCodeStatement(CStatement):

    def __init__(self, identifier: str):  # TODO VALIDATE IDENTIFIER INCLUDES STANDARD CHARACTERS
        super(UserCodeStatement, self).__init__(self._render)
        self.identifier = identifier
        self.content = ""  # TODO SCAN

    def _render(self, style: 'Style' = default_style) -> str:
        return (
            f"{style.user_code_begin(self.identifier)}\n"
            f"{self.content}"
            f"{style.user_code_end(self.identifier)}"
        )
