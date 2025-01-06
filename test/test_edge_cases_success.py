import pytest
import autopep8


class TestSuccessEdgeCases:
    def test_line_comment_with_do(self, dopy):
        input_string = """
            print('start')  # a comment with do
            print('not a block')
        """
        assert (
            dopy.preprocess(input_string).strip()
            == autopep8.fix_code(input_string).strip()
        )

    def test_nested_blocks_on_same_line(self, dopy):
        input_str = """
            if x do if y do print('double') end end
            print('after')
        """

        expected_string = """
            if x:
                if y:
                    print('double')
        """

        assert dopy.preprocess(input_str) == expected_string

    def test_decorator_string(self, dopy):
        input_str = """
        @decorator
        def func() do
            pass
        end
        """
        expected_string = """
        @decorator
        def func():
            pass
        """
        assert dopy.preprocess(input_str) == autopep8.fix_code(expected_string).lstrip()

    def test_implicit_concatenation(self, dopy):
        input_str = """
            message = "if x " "something" "do"
            print(message)
        """
        assert dopy.preprocess(input_str) == autopep8.fix_code(input_str).strip()

    def test_triple_quotes_with_escaped_quotes(self, dopy):
        input_str = """
        if x do \''' nested quote
            print("test")
        end
        """
        assert dopy.preprocess(input_str) == autopep8.fix_code(input_str).strip()
