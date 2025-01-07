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
- Preserves string literals and comments
- Processes .dopy files into pep8 compliant .py files (maintaining the dir structure)
- Recursively transpiles imports

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

More examples in the [examples](./examples/) dir

### cli

`dopy my_module.dopy`

Will use the current active python interpreter, can be overridden with `PYTHON_PATH` env var

## Flags

`-h --help`: Print help text

`-k --keep`: Keep transpiled python files in place (will overwrite)

`-d --dry-run`: Print the transpiled python code to console and exit

`-c --check`: Check dopy syntax without transpiling

## Syntax Rules

- Make sure the `do` keyword is on the same line as rest of the block declaration,
- `end` should be on its own line
- all imports at the top of the module
- must create a `__init__.py` file in dirs so that the transpiled python modules can be recognised

## Acknowledgements

This project is hugely inspired by [`mathialo/bython`](https://github.com/mathialo/bython)

### Todo

- [ ] support type hints
- [ ] `py2dopy` script
- [ ] function level imports
- [ ] nvim-treesitter support

### License

See [LICENSE](./LICENSE)
