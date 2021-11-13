from enum import Enum
from textwrap import indent
from typing import List, Union, Optional


class Style:
    check_hungarian = False

    class GroupDelimitatorStyle:
        """open or close brackets or parentheses style"""

        def __init__(self,
                     new_line_open_before: bool,
                     new_line_open_after: bool,
                     new_line_close_before: bool,
                     new_line_close_after: bool,
                     space_open_before: bool,
                     space_open_after: bool,
                     space_close_before: bool,
                     space_close_after: bool
                     ):
            self.new_line_open_before = new_line_open_before
            self.new_line_open_after = new_line_open_after
            self.new_line_close_before = new_line_close_before
            self.new_line_close_after = new_line_close_after
            self.space_open_before = space_open_before
            self.space_open_after = space_open_after
            self.space_close_before = space_close_before
            self.space_close_after = space_close_after

    _default_statement_bracket = {
        'new_line_open_before': True,
        'new_line_open_after': True,
        'new_line_close_before': True,
        'new_line_close_after': True,
        'space_open_before': False,
        'space_open_after': False,
        'space_close_before': False,
        'space_close_after': False
    }

    _default_declaration_bracket = {
        'new_line_open_before': True,
        'new_line_open_after': True,
        'new_line_close_before': True,
        'new_line_close_after': False,
        'space_open_before': False,
        'space_open_after': False,
        'space_close_before': False,
        'space_close_after': False
    }

    _default_parentheses = {
        'new_line_open_before': False,
        'new_line_open_after': False,
        'new_line_close_before': False,
        'new_line_close_after': False,
        'space_open_before': False,
        'space_open_after': False,
        'space_close_before': False,
        'space_close_after': False
    }

    # Function
    function_bracket = GroupDelimitatorStyle(**_default_statement_bracket)  # type: ignore
    function_definition_parentheses = GroupDelimitatorStyle(**_default_parentheses)  # type: ignore
    function_declaration_parentheses = GroupDelimitatorStyle(**_default_parentheses)  # type: ignore
    function_new_line_after_type_declaration = True
    function_space_after_name_definition = False
    function_space_after_name_declaration = False
    function_void_when_no_arguments = True
    function_indent_content = True

    # Struct
    struct_bracket = GroupDelimitatorStyle(**_default_declaration_bracket)  # type: ignore
    struct_new_line_members = True
    struct_indent_members = True
    struct_space_members = False

    # Union
    union_bracket = GroupDelimitatorStyle(**_default_declaration_bracket)  # type: ignore
    union_new_line_members = True
    union_space_members = False

    # Class
    class_bracket = GroupDelimitatorStyle(**_default_declaration_bracket)  # type: ignore
    class_indent_members = True
    class_indent_access = False

    # If
    if_bracket = GroupDelimitatorStyle(**_default_statement_bracket)  # type: ignore
    if_parentheses = GroupDelimitatorStyle(**_default_parentheses)  # type: ignore
    if_indent_content = True
    if_space_after_token = True

    # Else if
    else_if_bracket = GroupDelimitatorStyle(**_default_statement_bracket)  # type: ignore
    else_if_parentheses = GroupDelimitatorStyle(**_default_parentheses)  # type: ignore
    else_if_indent_content = True
    else_if_space_after_token = True

    # Else
    else_bracket = GroupDelimitatorStyle(**_default_statement_bracket)  # type: ignore
    else_indent_content = True
    else_space_after_token = True

    # Switch
    switch_bracket = GroupDelimitatorStyle(**_default_statement_bracket)  # type: ignore
    switch_parentheses = GroupDelimitatorStyle(**_default_parentheses)  # type: ignore
    switch_indent_content = True
    switch_indent_case_content = True
    switch_space_after_token = True

    # While
    while_bracket = GroupDelimitatorStyle(**_default_statement_bracket)  # type: ignore
    while_parentheses = GroupDelimitatorStyle(**_default_parentheses)  # type: ignore
    while_indent_content = True
    while_space_after_token = True

    # Do while
    do_while_bracket = GroupDelimitatorStyle(**_default_statement_bracket)  # type: ignore
    do_while_parentheses = GroupDelimitatorStyle(**_default_parentheses)  # type: ignore
    do_while_indent_content = True
    do_while_space_after_token = True

    # For
    for_bracket = GroupDelimitatorStyle(**_default_statement_bracket)  # type: ignore
    for_parentheses = GroupDelimitatorStyle(**_default_parentheses)  # type: ignore
    for_indent_content = True
    for_space_before_semicolon = False
    for_space_after_semicolon = True
    for_spaces_if_void = False
    for_space_after_token = True

    # Cast
    space_after_cast = False

    # Operators
    space_unary_operator = False
    space_before_binary_operator = True
    space_after_binary_operator = True
    space_before_parentheses_operator = False
    space_after_parentheses_operator = False

    # Statements
    space_before_semicolon_break_statement = False
    space_before_semicolon_continue_statement = False
    space_before_semicolon_return_statement = False

    # Attributes
    attribute_packed = "__attribute__((__packed__))"

    # Class member styles
    class ClassMembers(Enum):
        inline_access_preserve_order = 0
        group_by_access_specified = 1

    class_members = ClassMembers.group_by_access_specified

    # Literals
    literal_unsigned_token = "U"
    literal_long_token = "L"
    literal_float_token = "f"
    literal_double_token = "d"
    literal_boolean_true_token = "true"
    literal_boolean_false_token = "false"

    literal_hexadecimal_uppercase = True

    # Operators
    class NotOperatorsStyles(Enum):
        Exclamation = "!"
        Explicit = "not"

    class AndOperatorStyles(Enum):
        DoubleAmpersand = "&&"
        Explicit = "and"

    class OrOperatorStyles(Enum):
        DoubleVerticalBar = "||"
        Explicit = "or"

    not_operator_style = NotOperatorsStyles.Exclamation
    and_operator_style = AndOperatorStyles.DoubleAmpersand
    or_operator_style = OrOperatorStyles.DoubleVerticalBar

    # General tokens
    new_line_token = '\n'
    indent_token = '\t'
    space_token = ' '
    bracket_open_token = '{'
    bracket_close_token = '}'
    parentheses_open_token = '('
    parentheses_close_token = ')'

    def space(self, active: bool = True) -> str:
        return self.space_token if active else ''

    def new_line(self, active: bool = True) -> str:
        return self.new_line_token if active else ''

    def indent(self, value: str, active: bool = True) -> str:
        return indent(value, self.indent_token) if active else value

    def open_bracket(self, group_style: GroupDelimitatorStyle):
        return (
            f"{self.new_line(group_style.new_line_open_before)}"
            f"{self.space(group_style.space_open_before)}"
            f"{self.bracket_open_token}"
            f"{self.new_line(group_style.new_line_open_after)}"
            f"{self.space(group_style.space_open_before)}"
        )

    def close_bracket(self, group_style: GroupDelimitatorStyle):
        return (
            f"{self.new_line(group_style.new_line_close_before)}"
            f"{self.space(group_style.space_close_before)}"
            f"{self.bracket_close_token}"
            f"{self.new_line(group_style.new_line_close_after)}"
            f"{self.space(group_style.space_close_before)}"
        )

    def open_parentheses(self, group_style: GroupDelimitatorStyle):
        return (
            f"{self.new_line(group_style.new_line_open_before)}"
            f"{self.space(group_style.space_open_before)}"
            f"{self.parentheses_open_token}"
            f"{self.new_line(group_style.new_line_open_after)}"
            f"{self.space(group_style.space_open_before)}"
        )

    def close_parentheses(self, group_style: GroupDelimitatorStyle):
        return (
            f"{self.new_line(group_style.new_line_close_before)}"
            f"{self.space(group_style.space_close_before)}"
            f"{self.parentheses_close_token}"
            f"{self.new_line(group_style.new_line_close_after)}"
            f"{self.space(group_style.space_close_before)}"
        )

    @staticmethod
    def check_hungarian_variable(variable_name: str, hungarian_prefixes: Union[List[str], str]) -> bool:
        if isinstance(hungarian_prefixes, str):
            hungarian_prefixes = [str(hungarian_prefixes)]

        for hungarian_prefix in hungarian_prefixes:
            if variable_name.startswith(hungarian_prefix):
                start_letter = variable_name[len(hungarian_prefix)]
                if start_letter.isupper():
                    return True

        return False

    # Doxygen
    doc_doxygen_start_block = "/**"
    doc_doxygen_line_block = " * "
    doc_doxygen_end_block = " */"

    doc_doxygen_command_token = "@"

    def doxygen_format(self, lines: List[str]) -> str:
        if len(lines) == 0:
            return ""
        elif len(lines) == 1:
            return f"{self.doc_doxygen_start_block} {lines[0]}{self.doc_doxygen_end_block}{self.new_line_token}"
        else:
            content = ''.join([f"{self.doc_doxygen_line_block}{line}{self.new_line_token}" for line in lines])
            return (
                f"{self.doc_doxygen_start_block}{self.new_line_token}"
                f"{content}"
                f"{self.doc_doxygen_end_block}{self.new_line_token}"
            )

    def doxygen_command(self, command_name: str) -> str:
        return f"{self.doc_doxygen_command_token}{command_name}"


default_style = Style()
