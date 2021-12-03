from typing import TYPE_CHECKING, Union, List, Callable, Dict

from .statements import CDeclarations, CDeclaration, CStatement
from .style import default_style

from os.path import isfile, dirname
from os import makedirs
import re

if TYPE_CHECKING:
    from .style import Style

UserCodeCallback = Callable[['Style', str], str]


class File:
    """File Object"""

    def __init__(self,
                 declarations: Union['CDeclarations', List['CDeclaration']],
                 style: 'Style' = default_style):
        """Constructor

        Args:
            declarations: declarations in the file
            style:
        """
        if isinstance(declarations, CDeclaration):
            self.declarations = declarations
        else:
            self.declarations = CDeclarations(declarations)
        self.style = style

    def generate(self, path: str, auto_create_folders: bool = True) -> None:
        """Generate code in path

        Args:
            path: path of the file to generate
            auto_create_folders: if true, if the path specified does not exist, will create the folder tree required
        """
        generated = self.declarations.render()

        if isfile(path):
            # File already exist, scan current user code sections
            current_code_sections = {}
            with open(path, "r") as current:
                current_content = current.read()
                current_code_sections = self._analyze_code_sections(current_content)

            code_with_sections = self._insert_code_sections(generated, current_code_sections)
        else:
            # File does not exist, generate
            code_with_sections = generated

            if auto_create_folders:
                makedirs(dirname(path), exist_ok=True)

        with open(path, "w+") as output:
            output.write(code_with_sections)

    def _insert_code_sections(self, code: str, sections: Dict[str, str]) -> str:
        """Insert content to each code section

        Args:
            code: code to insert the code sections content
            sections: dictionary of sections with identifier as key and content of code section as value

        Returns:
            str: code with content inserted to code sections
        """
        generated_code_sections = self._analyze_code_sections(code)

        for identifier, _ in generated_code_sections.items():
            if identifier in sections.keys():
                code = re.sub(
                    # Find Pattern
                    self.user_code_pattern(identifier),

                    # Replace with
                    render_user_code_section(
                        identifier=identifier,
                        content=sections[identifier],
                        style=self.style
                    ),

                    # On this content
                    code
                )
        return code

    def _analyze_code_sections(self, content: str) -> Dict[str, str]:
        """Analyze and extract code section in a content

        Args:
            content: code content

        Returns:
            dictionary of sections with identifier as key and content of code section as value
        """
        code_sections = {}

        for section_match in re.finditer(self.user_code_pattern(), content):

            section = section_match.group()
            begin_token = re.search(self.any_begin_pattern(), section).group()
            end_token = re.search(self.any_end_pattern(), section).group()

            begin_id = begin_token \
                .lstrip(self.style.user_section_begin_pattern_before) \
                .rstrip(self.style.user_section_begin_pattern_after)

            end_id = end_token \
                .lstrip(self.style.user_section_end_pattern_before) \
                .rstrip(self.style.user_section_end_pattern_after)

            if begin_id != end_id:
                # TODO Info of content, line....
                raise ValueError("Code sections identifiers do not match")

            if begin_id in code_sections:
                # TODO Info of content, line....
                raise KeyError(f"identifier {begin_id} is duplicated")

            code_sections[begin_id] = section \
                .lstrip(self.style.user_section_begin(begin_id)) \
                .rstrip(self.style.user_section_end(begin_id))

        return code_sections

    def any_begin_pattern(self) -> str:
        return self.style.user_section_begin_pattern(r'(.*)')  # TODO REMOVE

    def any_end_pattern(self) -> str:
        return self.style.user_section_end_pattern(r'(.*)')

    def user_code_pattern(self, identifier: str = r'(.*)') -> str:  # TODO Move to style
        # Defaults to any
        return (
            rf"{self.style.user_section_begin_pattern(identifier)}"
            rf"(.|\n|\r|\t)*?"  # Any content between
            rf"{self.style.user_section_end_pattern(identifier)}"
        )


# TODO USER CODE NAME REFACTOR
def render_user_code_section(identifier: str, content: str, style: 'Style') -> str:
    """Render user section

    Args:
        identifier: identifier of the user section
        content: content of the section
        style: style to generate the begin and end

    Returns:
        str: generated user section
    """
    return (
        f"{style.user_section_begin(identifier)}"
        f"{content}"
        f"{style.user_section_end(identifier)}"
    )


class UserSectionStatement(CStatement):

    def __init__(self, identifier: str, default_content: str = "\n"):
        """Constructor

        Args:
            identifier: identifier of user code statement
            default_content:
        """
        # TODO VALIDATE IDENTIFIER INCLUDES STANDARD CHARACTERS
        # TODO Validate is unique to... file....??
        super(UserSectionStatement, self).__init__(self._render)
        self.identifier = identifier
        self.default_content = default_content

    def _render(self, style: 'Style' = default_style) -> str:
        """Render Code Section"""
        return render_user_code_section(
            identifier=self.identifier,
            content=self.default_content,
            style=style
        )
