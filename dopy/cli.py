import argparse
from dopy.help import HELP_TEXT
from dopy.core import Dopy
from dopy.exceptions import DopyUnmatchedBlockError
import autopep8

dopy = Dopy()

"""
cli interface
"""


def _save_to_file(contents: str, name: str):
    """write the processed python string to file"""
    try:
        with open(name, "w") as f:
            f.write(contents)
    except Exception as e:
        print(f"Error writing to file: {e}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Python without indentation", add_help=False
    )
    # Create a mutually exclusive group that allows a single flag at a time
    group = parser.add_mutually_exclusive_group()

    group.add_argument(
        "--keep",
        "-k",
        action="store_true",
        help="Transpile modules in place, preserving dir structure",
    )
    group.add_argument(
        "--dry-run",
        "-d",
        action="store_true",
        help="Dry run, print transpiled result to the console and exit",
    )

    group.add_argument(
        "--check", "-c", action="store_true", help="Check syntax without transpiling"
    )

    group.add_argument("--help", "-h", action="store_true", help="Show help text")

    parser.add_argument("target", nargs="?", help="Target dopy module name")
    args = parser.parse_args()

    if args.help:
        print(HELP_TEXT)
        return

    contents = None
    processed_with_pep8 = None

    try:
        with open(args.target, "r") as f:
            contents = f.read()
        processed = dopy.preprocess(contents)
        processed_with_pep8 = autopep8.fix_code(processed)
    except FileNotFoundError:
        print(f"Error: Target {args.target} not found.")

    if not args.target:
        print("Error: Target module not specified.")

    if args.check:
        try:
            dopy.validate_syntax(contents)
            print(f"✓ {args.target} syntax is valid")
            return 0
        except DopyUnmatchedBlockError as e:
            print(f"✗ Syntax Error in {args.target}: {str(e)}")
            return 1

    if args.keep:
        _save_to_file(processed, args.target[:-5] + ".py")
    if args.dry_run:
        print(processed_with_pep8)
        return
    try:
        namespace = {}
        exec(processed_with_pep8, namespace)
    except Exception as e:
        print(f"Error running transpiled code : {e}")


if __name__ == "__main__":
    main()
