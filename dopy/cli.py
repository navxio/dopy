import argparse
from dopy.core import preprocess_do_end as preprocess
from dopy.help import HELP_TEXT

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
        "-t",
        action="store_true",
        help="Transpile modules in place, preserving dir structure",
    )

    group.add_argument(
        "-T", nargs="?", const=True, help="Transpile module to optional target_name.py"
    )

    group.add_argument("-h", action="store_true", help="Show help text")
    args = parser.parse_args()

    if args.h:
        print(HELP_TEXT)


if __name__ == "__main__":
    main()
