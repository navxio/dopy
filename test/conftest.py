import pytest
from dopy.core import Dopy


@pytest.fixture(scope="class")
def dopy():
    """
    Class-scoped fixture providing a shared Dopy instance.
    Available to all test modules in the test directory and subdirectories.

    Returns:
        Dopy: A Dopy preprocessor instance

    Example:
        def test_something(self, dopy):
            result = dopy.preprocess("some code")
    """
    dopy_instance = Dopy()
    yield dopy_instance
    # Reset state after each test class
    dopy_instance.indent_level = 0
    dopy_instance.indent_stack = []
    dopy_instance.paren_level = 0
    dopy_instance.in_multiline_string = False
    dopy_instance.quote_char = None
