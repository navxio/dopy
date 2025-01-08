from dopy.exceptions import DopyFileError, DopyUnmatchedBlockError


class Dopy:
    """
    Dopy is a preprocesor for python that removes the need for strict
    indentation by supplanting them with indentation agnostic do..end blocks
    """

    def __init__(self):
        self.indent_level = 0
        self.block_stack = []

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

    def validate_syntax(self, code):
        """Validate do/end block matching"""
        lines = code.split("\n")
        self.block_stack = []

        for line_num, line in enumerate(lines, 1):
            stripped = line.strip()

            # Skip empty lines
            if not stripped:
                continue

            # Skip comments
            if stripped.startswith("#"):
                continue

            # Check if we're in a string to avoid matching do/end within strings
            if self._is_in_string(stripped, len(stripped) - 3):
                continue

            # Check for blocks
            if stripped.startswith("end"):
                if not self.block_stack:
                    raise DopyUnmatchedBlockError(f"Unmatched 'end' at line {line_num}")
                self.block_stack.pop()

            if stripped.endswith("do") and "#" not in stripped:
                self.block_stack.append((stripped, line_num))

            # comment case
            do_index = stripped.find("do")
            comment_start_index = stripped.find("#")

            if do_index != -1 and do_index < comment_start_index:
                self.block_stack.append((stripped, line_num))

        if self.block_stack:
            unclosed = self.block_stack[-1]
            raise DopyUnmatchedBlockError(
                f"Unclosed 'do' block starting at line {unclosed[1]}: '{unclosed[0]}'"
            )

    def _process_line(self, line) -> str:
        """process a single line"""
        if not line.strip():
            return None

        stripped = line.strip()

        if stripped.endswith("do"):
            if "#" in stripped:
                return stripped
            doless_line = stripped.replace(" do", ":")
            result = "    " * self.indent_level + doless_line.strip()
            self.indent_level += 1
            return result
        elif stripped.find("do") < stripped.find("#"):
            # both comment and do in the same line
            doless_line = stripped.replace(" do", ":")
            result = "    " * self.indent_level + doless_line.strip()
            self.indent_level += 1
            return result
        elif stripped.endswith("end") and "#" not in stripped:
            self.indent_level -= 1
            return ""
        else:
            return "    " * self.indent_level + stripped

    def preprocess(self, code):
        """Main preprocessing method"""
        # Reset state
        self.indent_level = 0
        self.block_stack = []

        # normalize line endings
        code = code.replace("\r\n", "\n").replace("\r", "\n")

        self.validate_syntax(code)

        lines = code.split("\n")

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
        try:
            with open(input_file, "r") as f:
                code = f.read()
        except Exception as e:
            raise DopyFileError(input_file, "read", e)

        processed = self.preprocess(code)

        if output_file:
            try:
                with open(output_file, "w") as f:
                    f.write(processed)
            except Exception as e:
                raise DopyFileError(output_file, "write", e)
            return True
        return processed
