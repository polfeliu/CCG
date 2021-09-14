class Style:
    check_hungarian = False

    # New lines
    new_line_function_bracket_open_before = False
    new_line_function_bracket_open_after = False
    new_line_function_bracket_close_before = False
    new_line_function_bracket_close_after = False

    new_line_function_prototype_type = False

    @property
    def _new_line_function_bracket_open_before(self):
        return "\n" if self.new_line_function_bracket_open_before else ''

    @property
    def _new_line_function_bracket_open_after(self):
        return '\n' if self.new_line_function_bracket_open_after else ''

    @property
    def _new_line_function_bracket_close_before(self):
        return '\n' if self.new_line_function_bracket_close_before else ''

    @property
    def _new_line_function_bracket_close_after(self):
        return '\n' if self.new_line_function_bracket_close_after else ''

    @property
    def _new_line_function_prototype_type(self):
        return '\n' if self.new_line_function_prototype_type else ''

    # Spaces
    space_function_after_name_prototype = True
    space_function_after_name_declaration = True

    @property
    def _space_function_after_name_prototype(self):
        return ' ' if self.space_function_after_name_prototype else ''

    @property
    def _space_function_after_name_declaration(self):
        return ' ' if self.space_function_after_name_declaration else ''


default_style = Style()

asdf = 1
