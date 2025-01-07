import autopep8


class TestSuccess:
    def test_dopy_function_success(self, dopy):
        input_code_string = """
        def my_func() do
            print("hello world")
        end
        """
        expected_string = """
def my_func():
    print("hello world")
"""
        assert (
            dopy.preprocess(input_code_string)
            == autopep8.fix_code(expected_string).lstrip()
        )

    def test_dopy_if_else(self, dopy):
        input_code_string = """
            if (True) do
                print('true')
            end
        """
        expected_string = """
if (True):
    print('true')
"""
        assert (
            dopy.preprocess(input_code_string)
            == autopep8.fix_code(expected_string).lstrip()
        )

    def test_dopy_classes(self, dopy):
        input_code_str = """
            class MyClass do
                def __init__(self) do
                    self.x = 0
                end
                pass
            end
        """
        expected_string = """
class MyClass:
    def __init__(self):
        self.x = 0

    pass
"""

        assert (
            dopy.preprocess(input_code_str)
            == autopep8.fix_code(expected_string).lstrip()
        )

    def test_while_loop(self, dopy):
        input_code_str = """
        while True do
            print('true')
        end
        """
        expected_output = """
while True:
    print('true')
        """
        assert (
            dopy.preprocess(input_code_str)
            == autopep8.fix_code(expected_output).lstrip()
        )

    def test_for_loop(self, dopy):
        input_code_str = """
        for i in range(42) do
            print(i)
        end
        """
        expected_output = """
for i in range(42):
    print(i)
        """
        assert (
            dopy.preprocess(input_code_str)
            == autopep8.fix_code(expected_output).lstrip()
        )

    def test_context_manager(self, dopy):
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
        assert dopy.preprocess(input_str) == autopep8.fix_code(expected_output).lstrip()

    def test_exception_handling(self, dopy):
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

        expected_string = """
try:
    print('tried')

except:
    print('except')

else:
    print('else')

finally:
    print('finally')

            """

        assert dopy.preprocess(input_str) == autopep8.fix_code(expected_string).lstrip()

    def test_match(self, dopy):
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
        expected_string = """
match value:
    case pattern1:
        pass

    case pattern2:
        pass
"""
        assert (
            dopy.preprocess(input_str).strip()
            == autopep8.fix_code(expected_string).strip()
        )
