import pytest
import autopep8


class TestDopyHints:
    def normalize(self, code: str) -> str:
        """Normalize code using autopep8 for consistent formatting"""
        return autopep8.fix_code(code).strip()

    def test_basic_function_type_hints(self, dopy):
        code = """
def greet(name: str) -> str do
    return f"Hello {name}"
end
"""
        expected = """
def greet(name: str) -> str:
    return f"Hello {name}"
"""
        assert self.normalize(dopy.preprocess(code)) == self.normalize(expected)

    def test_complex_type_hints(self, dopy):
        code = """
def process_data(items: List[Dict[str, Any]], flag: Optional[bool] = None) -> Tuple[List[int], str] do
    return [], ""
end
"""
        expected = """
def process_data(items: List[Dict[str, Any]], flag: Optional[bool] = None) -> Tuple[List[int], str]:
    return [], ""
"""
        assert self.normalize(dopy.preprocess(code)) == self.normalize(expected)

    def test_variable_annotations(self, dopy):
        code = """
def initialize() do
    count: int = 0
    names: List[str] = []
    mapping: Dict[str, Union[int, str]] = {}
end
"""
        expected = """
def initialize():
    count: int = 0
    names: List[str] = []
    mapping: Dict[str, Union[int, str]] = {}
"""
        assert self.normalize(dopy.preprocess(code)) == self.normalize(expected)

    def test_nested_function_type_hints(self, dopy):
        code = """
def outer(x: int) -> callable do
    def inner(y: float) -> float do
        return x + y
    end
    return inner
end
"""
        expected = """
def outer(x: int) -> callable:
    def inner(y: float) -> float:
        return x + y

    return inner
"""
        assert self.normalize(dopy.preprocess(code)) == self.normalize(expected)

    def test_class_method_type_hints(self, dopy):
        code = """
class DataProcessor do
    def process(self, data: List[str]) -> Dict[str, int] do
        return {}
    end
    
    @classmethod
    def from_file(cls, path: str) -> "DataProcessor" do
        return cls()
    end
end
"""
        expected = """
class DataProcessor:
    def process(self, data: List[str]) -> Dict[str, int]:
        return {}
    
    @classmethod
    def from_file(cls, path: str) -> "DataProcessor":
        return cls()
"""
        assert self.normalize(dopy.preprocess(code)) == self.normalize(expected)

    def test_async_function_type_hints(self, dopy):
        code = """
async def fetch_data(url: str) -> Optional[Dict[str, Any]] do
    return None
end
"""
        expected = """
async def fetch_data(url: str) -> Optional[Dict[str, Any]]:
    return None
"""
        assert self.normalize(dopy.preprocess(code)) == self.normalize(expected)

    def test_generic_type_hints(self, dopy):
        code = """
def identity[T](value: T) -> T do
    return value
end
"""
        expected = """
def identity[T](value: T) -> T:
    return value
"""
        assert self.normalize(dopy.preprocess(code)) == self.normalize(expected)

    def test_multiline_type_hints(self, dopy):
        code = """
def complex_types(
    data: List[
        Dict[str, Union[int, str, None]]
    ]
) -> Optional[
    Tuple[List[int], str]
] do
    return None
end
"""
        expected = """
def complex_types(
    data: List[
        Dict[str, Union[int, str, None]]
    ]
) -> Optional[
    Tuple[List[int], str]
]:
    return None
"""
        assert self.normalize(dopy.preprocess(code)) == self.normalize(expected)

    @pytest.mark.edge
    def test_type_hints_with_comments(self, dopy):
        code = """
def process(
    data: List[str],  # list of strings to process
    count: int = 0    # number of items to process
) -> Dict[str, Any] do  # returns processed data
    return {}
end
"""
        expected = """
def process(
    data: List[str],  # list of strings to process
    count: int = 0    # number of items to process
) -> Dict[str, Any]:  # returns processed data
    return {}
"""
        assert self.normalize(dopy.preprocess(code)) == self.normalize(expected)
