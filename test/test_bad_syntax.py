import pytest
from dopy.exceptions import DopyUnmatchedBlockError, DopyFileError


class TestDopyBadSyntax:
    def test_unmatched_do_block(self, dopy):
        """Test that an unmatched 'do' block raises the appropriate exception"""
        code = """
def calculate() do
    x = 10
    if x > 5 do
        print("Greater than 5")
    # Missing end for if block
# Missing end for calculate block
        """
        with pytest.raises(DopyUnmatchedBlockError) as exc_info:
            dopy.preprocess(code)
        assert "Unmatched Unclosed 'do' block" in str(exc_info.value)

    def test_unmatched_end_block(self, dopy):
        """Test that an unmatched 'end' block raises the appropriate exception"""
        code = """
def calculate() do
    x = 10
    if x > 5 do
        print("Greater than 5")
    end
end
end  # Extra end statement
        """
        with pytest.raises(DopyUnmatchedBlockError) as exc_info:
            dopy.preprocess(code)
        assert "Unmatched 'end' at" in str(exc_info.value)

    def test_inexistent_input_file(self, dopy):
        """Test that attempting to process a non-existent file raises the appropriate exception"""
        with pytest.raises(DopyFileError) as exc_info:
            dopy.process_file("nonexistent_file.dopy")
        assert "Could not read file" in str(exc_info.value)
        assert "nonexistent_file.dopy" in str(exc_info.value)
