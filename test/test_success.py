import pytest
from dopy.core import Dopy

dopy = Dopy()


@pytest.mark.edge
class TestSuccess:
    def test_dopy_function_success(self):
        input_code_string = """
        def my_func() do
            print("hello world")
        end
        """
        expected_string = """
def my_func():
    print("hello world")
"""
        assert dopy.preprocess(input_code_string).strip() == expected_string.strip()

    def test_dopy_if_else(self):
        input_code_string = """
            if (True) do
                print('true')
            end
        """
        expected_string = """
if (True):
    print('true')
"""
        assert dopy.preprocess(input_code_string).strip() == expected_string.strip()

    def test_dopy_classes(self):
        input_code_str = """
            class MyClass do
                def __init__(self) do
                    self.x = 0
                end
                pass
            end
        """
        expected_output = """
class MyClass:
    def __init__(self):
        self.x = 0
    pass
"""

        assert dopy.preprocess(input_code_str).strip() == expected_output.strip()

    def test_while_loop(self):
        input_code_str = """
        while True do
            print('true')
        end
        """
        expected_output = """
while True:
    print('true')
        """
        assert dopy.preprocess(input_code_str).strip() == expected_output.strip()

    def test_for_loop(self):
        input_code_str = """
        for i in range(42) do
            print(i)
        end
        """
        expected_output = """
for i in range(42):
    print(i)
        """
        assert dopy.preprocess(input_code_str).strip() == expected_output.strip()

    def test_context_manager(self):
        input_str = """
            with open('target.txt') as f do
                # do something with f
            pass
            end
        """
        expected_output = """
with open('target.txt') as f:
    # do something with f
    pass
        """
        assert dopy.preprocess(input_str).strip() == expected_output.strip()

    def test_exception_handling(self):
        input_str = """
            try do
                print('tried')
            end
            except do
                print('except')
            end
            else do
                print('else')
            end
            finally do
                print('finally')
            end
        """

        expected_output = """
try:
    print('tried')
except:
    print('except')
else:
    print('else')
finally:
    print('finally')
            """

        assert dopy.preprocess(input_str).strip() == expected_output.strip()

    def test_match(self):
        input_str = """
            match value do
                case pattern1 do
                pass
                end
                case pattern2 do
                pass
                end
            end
        """
        expected_str = """
match value:
    case pattern1:
        pass
    case pattern2:
        pass
"""
        assert dopy.preprocess(input_str).strip() == expected_str.strip()
