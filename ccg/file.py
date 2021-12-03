from typing import TYPE_CHECKING, Union, List, Callable, Dict

from .statements import CDeclarations, CDeclaration, CStatement
from .style import default_style

from os.path import isfile, dirname
from os import makedirs
import re

if TYPE_CHECKING:
    from .style import Style

UserSectionCallback = Callable[['Style', str], str]


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
        if isinstance(declarations, CDeclarations):
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
            with open(path, "r") as current:
                current_code_sections = {}
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
                    self.style.user_section_pattern(identifier),

                    # Replace with
                    render_user_section(
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

        for section_match in re.finditer(self.style.user_section_pattern(), content):
            section = section_match.group()

            begin_token_search = re.search(
                self.style.user_section_begin_pattern(r'(.*)'),
                section
            )
            if begin_token_search is None:
                raise RuntimeError("Could not find begin token inside section")
            else:
                begin_token = begin_token_search.group()

            end_token_search = re.search(
                self.style.user_section_end_pattern(r'(.*)'),
                section
            )
            if end_token_search is None:
                raise RuntimeError("Could not find end token inside section")
            else:
                end_token = end_token_search.group()

            begin_id = begin_token \
                .lstrip(self.style.user_section_begin_pattern_before) \
                .rstrip(self.style.user_section_begin_pattern_after)

            end_id = end_token \
                .lstrip(self.style.user_section_end_pattern_before) \
                .rstrip(self.style.user_section_end_pattern_after)

            if begin_id != end_id:
                raise ValueError(f"Code sections identifiers do not match \n"
                                 f"begin id: {begin_id}\n"
                                 f"end id: {end_id}")

            if begin_id in code_sections:
                raise KeyError(f"Identifier {begin_id} is duplicated")

            code_sections[begin_id] = section \
                .lstrip(self.style.user_section_begin(begin_id)) \
                .rstrip(self.style.user_section_end(begin_id))

        return code_sections


def render_user_section(identifier: str, content: str, style: 'Style') -> str:
    """Render user section

    Args:
        identifier: identifier of the user section
        content: content of the section
        style: style to generate the begin and end

    Returns:
        str: generated user section
    """
    is_identifier_legal = re.match(
        pattern=style.user_section_identifier_pattern,
        string=identifier
    )

    if not is_identifier_legal:
        raise ValueError(f"Identifier {identifier} does not have a valid name")

    return (
        f"{style.user_section_begin(identifier)}"
        f"{content}"
        f"{style.user_section_end(identifier)}"
    )


class UserSection(CDeclaration):
    """User Section

    Allows creating sections in a file where the user can edit the file
        and the generation of code will not overwrite those changes

    Note:
        Inherits from declaration since it can be on the outer scope of a file, or as a statement inside the
         contents of a function for example (that contains statements, but declaration inherits from statement)
    """

    def __init__(self, identifier: str, default_content: str = "\n"):
        """Constructor

        Args:
            identifier: identifier of user section
            default_content:
        """
        super(UserSection, self).__init__(self._render)
        self.identifier = identifier
        self.default_content = default_content

    def _render(self, style: 'Style' = default_style) -> str:
        """Render Code Section"""
        return render_user_section(
            identifier=self.identifier,
            content=self.default_content,
            style=style
        )
