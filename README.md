# dopy

An experimental Python preprocessor that enables do..end syntax in place of strict indentation

## Requirements

- `python 3.10+`
- `pip`

## Installation

```bash
pip install dopy-cli
```

## Features

- Converts ruby/lua style `do..end` blocks into indented blocks
- Maintains python's semantics
- Handles both inline and multi line `do..end` blocks
- Preserves string literals and comments
- Processes .dopy files into pep8 compliant .py files (maintaining the dir structure)

## Usage

### Programmatic

```python
from dopy.core import Dopy
dopy = Dopy()

source = '''
def hello_world() do
  print("Hello")
end
hello_world()
'''

processed = dopy.preprocess(source)
exec(processed, namespace={})
```

### cli

`dopy my_module.dopy`
Will use the current active python interpreter, can be overridden with `PYTHON_PATH` env var

## Flags

`-h --help`: Print help text
`-k --keep`: Keep transpiled python files in place
`-d --dry-run`: Print the transpiled python code to console and exit
`-c --check`: Check dopy syntax without transpiling

## Syntax Rules

- Make sure the `do` keyword is on the same line as rest of the block declaration,
- `end` should be on its own line
- single line do..end blocks are supported but shouldn't be used liberally

## Acknowledgements

This project is hugely inspired by [`mathialo/bython`](https://github.com/mathialo/bython)

### Todo

- [ ] nvim-treesitter support
- [ ] github publish pipeline
- [ ] support type hints
- [ ] `py2dopy` script

### License

GPL-v2.0
