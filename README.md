# dopy

A Python preprocessor that enables do..end syntax.

## Installation

```bash
pip install dopy
```

## Usage

```python
from dopy import preprocess

source = '''
def example():
    do
        print("Hello")
    end
'''

processed = preprocess(source)
exec(processed)
```

## License

MIT License
