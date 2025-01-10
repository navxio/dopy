import argparse
from pathlib import Path
from dopy.help import HELP_TEXT
from dopy.core import Dopy
from dopy.exceptions import DopyUnmatchedBlockError
from dopy.run import run_without_files, run_with_files
import autopep8

dopy = Dopy()


def resolve_target_path(target: str) -> Path:
    """
    Resolve the target path, handling both relative and absolute paths.
    Ensures the target has .dopy extension.

    Args:
        target: The target filename or path provided via CLI

    Returns:
        Path: Resolved absolute path to the target .dopy file

    Raises:
        FileNotFoundError: If the target file doesn't exist
        ValueError: If the target doesn't have .dopy extension
    """
    # Convert to Path object
    target_path = Path(target)

    # Check file extension
    if target_path.suffix != ".dopy":
        raise ValueError("Target file must have .dopy extension")

    # If it's not absolute, make it absolute from current working directory
    if not target_path.is_absolute():
        target_path = Path.cwd() / target_path

    # Resolve any symbolic links and normalize path
    target_path = target_path.resolve()

    # Check if file exists
    if not target_path.exists():
        raise FileNotFoundError(f"Target file not found: {target_path}")

    return target_path


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
        "--stdout",
        "-s",
        action="store_true",
        help="Print transpiled result to the console and exit",
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

    if not args.target:
        print("Error: Target module not specified.")
        return 1

    try:
        # Resolve the target path
        target_path = resolve_target_path(args.target)

        if args.check:
            with open(target_path, "r") as f:
                contents = f.read()
            try:
                dopy.validate_syntax(contents)
                print(f"✓ {target_path} syntax is valid")
                return 0
            except DopyUnmatchedBlockError as e:
                print(f"✗ Syntax Error in {target_path}: {str(e)}")
                return 1

        if args.keep:
            run_with_files(main_module=target_path)
            return 0

        if args.stdout:
            with open(target_path, "r") as f:
                contents = f.read()
            try:
                processed = dopy.preprocess(contents)
                processed_with_pep8 = autopep8.fix_code(processed)
                print(processed_with_pep8)
                return 0
            except Exception as e:
                print(f"Error preprocessing code: {e}")
                return 1

        # Default case: run without keeping files
        run_without_files(main_module=target_path)
        return 0

    except FileNotFoundError as e:
        print(f"Error: {e}")
        return 1
    except ValueError as e:
        print(f"Error: {e}")
        return 1
    except Exception as e:
        print(f"Error: An unexpected error occurred: {e}")
        return 1


if __name__ == "__main__":
    exit(main())
