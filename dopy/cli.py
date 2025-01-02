import argparse
from dopy.help import HELP_TEXT
from dopy.core import Dopy

dopy = Dopy()

"""
cli interface
"""


def main():
    parser = argparse.ArgumentParser(
        description="Python without indentation", add_help=False
    )
    # Create a mutually exclusive group that allows a single flag at a time
    group = parser.add_mutually_exclusive_group()

    group.add_argument(
        "--transpile",
        "-t",
        action="store_true",
        help="Transpile modules in place, preserving dir structure",
    )

    group.add_argument("--help", "-h", action="store_true", help="Show help text")

    parser.add_argument("target", nargs="?", help="Target dopy module name")
    args = parser.parse_args()

    if args.help:
        print(HELP_TEXT)
        return

    if args.transpile:
        if args.target:
            try:
                with open(args.target, "r") as f:
                    contents = f.read()
                processed = dopy.preprocess(contents)
                exec(processed)
            except FileNotFoundError:
                print(f"Error: Target {args.target} not found.")
    else:
        print(HELP_TEXT)


if __name__ == "__main__":
    main()
