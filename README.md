# dopy

An experimental Python preprocessor that enables do..end syntax in addition to indented blocks

## Installation

```bash
pip install dopy-cli
```

## Features

- Converts ruby/lua style `do..end` blocks into indented blocks
- Maintains python's semantics while relaxing indentation requirements
- Handles both inline and multi line `do..end` blocks
- Preserves string literals and comments
- Processes .dopy files into valid .py files (maintaining the dir structure)

## Usage

### Programmatic

```python
from dopy import preprocess

source = '''
def example() do
        print("Hello")
    end
'''

processed = preprocess(source)
exec(processed)
```

### cli

`dopy my_module.dopy`
Will use the current active python interpreter, can be overridden with `PYTHON_PATH` env var

## Flags

`-h --help`: Print help text
`-t --transpile`: Produce transpiled python files in place

## Acknowledgements

This project is hugely inspired by [`mathialo/bython`](https://github.com/mathialo/bython)

### License

GPL-v2.0
