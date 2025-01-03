class Dopy:
    """
    Dopy is a preprocesor for python that removes the need for strict
    indentation by supplanting them with do..end blocks
    """

    def __init__(self):
        self.indent_level = 0
        self.indent_stack = []
        self.paren_level = 0
        self.in_multiline_string = False
        self.quote_char = None

    def _get_line_indent(self, line):
        """Get the indentation level of a line"""
        return len(line) - len(line.lstrip())

    def _count_unescaped_quotes(self, s, quote):
        """Count unescaped quotes in a string"""
        count = 0
        i = 0
        while i < len(s):
            if s[i] == "\\":
                i += 2
                continue
            if s[i] == quote:
                count += 1
            i += 1
        return count

    def _is_in_string(self, line, pos):
        """Check if position is inside a string"""
        single_count = self._count_unescaped_quotes(line[:pos], "'")
        double_count = self._count_unescaped_quotes(line[:pos], '"')
        return (single_count % 2 == 1) or (double_count % 2 == 1)

    def _handle_line_continuations(self, code):
        """Handle line continuations and multi-line strings"""
        lines = []
        current_line = []

        for line in code.split("\n"):
            stripped = line.lstrip()

            # Handle multi-line strings
            if not self.in_multiline_string:
                triple_single = stripped.count("'''")
                triple_double = stripped.count('"""')
                if triple_single % 2 == 1 or triple_double % 2 == 1:
                    self.in_multiline_string = True
                    self.quote_char = "'''" if triple_single else '"""'
            else:
                if self.quote_char in line:
                    self.in_multiline_string = False

            # Handle line continuations
            if current_line and current_line[-1].endswith("\\"):
                current_line[-1] = current_line[-1][:-1]
                current_line.append(line)
            else:
                if current_line:
                    lines.append("".join(current_line))
                    current_line = []
                if line.endswith("\\"):
                    current_line.append(line[:-1])
                else:
                    lines.append(line)

        if current_line:
            lines.append("".join(current_line))

        return lines

    def _process_line(self, line) -> str:
        """process a single line"""
        if not line.strip():
            return None

        stripped = line.strip()
        if stripped.endswith("do"):
            doless_line = stripped.replace("do", "")
            result = "    " * self.indent_level + doless_line.strip() + ":"
            self.indent_level += 1
            return result
        elif stripped.endswith("end"):
            self.indent_level -= 1
            return ""
        else:
            return "    " * self.indent_level + stripped

    def preprocess(self, code):
        """Main preprocessing method"""
        # Reset state
        self.indent_level = 0
        self.indent_stack = []
        self.paren_level = 0
        self.in_multiline_string = False
        self.quote_char = None

        # Handle line continuations and get cleaned lines
        lines = self._handle_line_continuations(code)

        # Process each line
        result = []
        for line in lines:
            processed = self._process_line(line)
            if processed is None:
                continue
            result.append(processed)

        return "\n".join(result)

    def process_file(self, input_file, output_file=None):
        """Process a file and optionally write to output file"""
        with open(input_file, "r") as f:
            code = f.read()

        processed = self.preprocess(code)

        if output_file:
            with open(output_file, "w") as f:
                f.write(processed)
            return True
        return processed
