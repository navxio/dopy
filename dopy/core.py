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

    def _process_line(self, line):
        """Process a single line of code"""
        if not line.strip():
            return "    " * self.indent_level + line

        current_indent = self._get_line_indent(line)
        stripped = line.lstrip()

        # Track parentheses
        self.paren_level += stripped.count("(") - stripped.count(")")

        # Handle multiple do..end on one line
        if ";" in stripped:
            sublines = stripped.split(";")
            result = []
            for subline in sublines:
                if subline.strip():
                    result.extend(self.preprocess(subline.strip()).split("\n"))
            return "\n".join(result)

        # Skip processing if we're in a multi-line string or parentheses block
        if self.in_multiline_string or self.paren_level > 0:
            return line

        # Handle inline do..end
        if " do " in stripped and " end" in stripped:
            do_pos = stripped.index(" do ")
            end_pos = stripped.index(" end")
            if not self._is_in_string(stripped, do_pos) and not self._is_in_string(
                stripped, end_pos
            ):
                processed = stripped.replace(" do ", ": ").replace(" end", "")
                return " " * current_indent + processed

        # Handle 'do' at end of line
        if stripped.endswith(" do") and not self._is_in_string(
            stripped, len(stripped) - 3
        ):
            self.indent_stack.append(current_indent)
            processed = line.replace(" do", ":")
            self.indent_level += 1
            return processed

        # Handle 'end'
        elif (
            stripped == "end" or stripped.startswith("end #")
        ) and not self._is_in_string(stripped, 0):
            if self.indent_stack:
                self.indent_level -= 1
                self.indent_stack.pop()
            return None

        # Regular lines
        else:
            base_indent = " " * current_indent
            nested_indent = "    " * (self.indent_level - len(self.indent_stack))
            return base_indent + nested_indent + stripped

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
            if processed is not None:  # Skip 'end' lines
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
