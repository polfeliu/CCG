from .union import Union


class Style:
    check_hungarian = False

    # New lines
    new_line_function_bracket_open_before = False
    new_line_function_bracket_open_after = False
    new_line_function_bracket_close_before = False
    new_line_function_bracket_close_after = False

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



default_style = Style()
