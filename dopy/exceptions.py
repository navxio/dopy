class DopyError(Exception):
    """Base exception class for all Dopy-related errors."""

    def __init__(self, message: str, line_number: int = None, line_content: str = None):
        self.line_number = line_number
        self.line_content = line_content
        self.message = self._format_message(message)
        super().__init__(self.message)

    def _format_message(self, message: str) -> str:
        """Format the error message with line information if available."""
        if self.line_number is not None and self.line_content is not None:
            return f"{message}\nAt line {self.line_number}: {self.line_content}"
        return message


class DopySyntaxError(DopyError):
    """Raised when there's a syntax error in the Dopy code."""

    def __init__(self, message: str, line_number: int = None, line_content: str = None):
        super().__init__(f"Syntax Error: {message}", line_number, line_content)


class DopyUnmatchedBlockError(DopySyntaxError):
    """Raised when there's an unmatched do/end block."""

    def __init__(
        self, block_type: str, line_number: int = None, line_content: str = None
    ):
        super().__init__(f"Unmatched {block_type} block", line_number, line_content)


class DopyParsingError(DopyError):
    """Raised when there's an error parsing the Dopy code."""

    def __init__(self, message: str, line_number: int = None, line_content: str = None):
        super().__init__(f"Parsing Error: {message}", line_number, line_content)


class DopyStringError(DopyParsingError):
    """Raised when there's an error with string literals."""

    def __init__(self, message: str, line_number: int = None, line_content: str = None):
        super().__init__(f"String Error: {message}", line_number, line_content)


class DopyFileError(DopyError):
    """Raised when there's an error with file operations."""

    def __init__(self, filename: str, operation: str, original_error: Exception = None):
        message = f"File Error: Could not {operation} file '{filename}'"
        if original_error:
            message += f"\nCause: {str(original_error)}"
        super().__init__(message)
