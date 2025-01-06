import pytest
from dopy.core import Dopy
from dopy.exceptions import DopyUnmatchedBlockError, DopyFileError


class TestDopyBadSyntax:
    @pytest.mark.edge
    def test_unmatched_do_block(self):
        """Test that an unmatched 'do' block raises the appropriate exception"""
        dopy = Dopy()
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
        assert "Unmatched do block" in str(exc_info.value)

    def test_unmatched_end_block(self):
        """Test that an unmatched 'end' block raises the appropriate exception"""
        dopy = Dopy()
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
        assert "Unmatched end block" in str(exc_info.value)

    def test_inexistent_input_file(self):
        """Test that attempting to process a non-existent file raises the appropriate exception"""
        dopy = Dopy()
        with pytest.raises(DopyFileError) as exc_info:
            dopy.process_file("nonexistent_file.dopy")
        assert "Could not read file" in str(exc_info.value)
        assert "nonexistent_file.dopy" in str(exc_info.value)
