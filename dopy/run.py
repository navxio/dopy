from pathlib import Path
import tempfile
import importlib.util
import sys
from typing import Union
from dopy.core import Dopy
from dopy.transpiler import process_with_imports
from dopy.transpiler.collector import DopyImportCollector


def run_module(module_path: str):
    """Run a Python module dynamically from a file path."""
    # Convert module path to module name (e.g., './foo.py' -> 'foo')
    module_name = Path(module_path).stem

    # Create and load the module spec
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)

    # Add module to sys.modules
    sys.modules[module_name] = module

    # Execute the module
    spec.loader.exec_module(module)


def run_without_files(main_module: Union[str, Path], project_root: Path = None, dopy: Dopy) -> None:
    """
    Run Dopy code without creating permanent files by using a temporary directory.

    Args:
        main_module: Path to the main .dopy file to execute
        project_root: Optional root directory for resolving imports
    """
    main_module = Path(main_module)
    if project_root is None:
        project_root = main_module.parent

    # Create temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_dir = Path(temp_dir)

        # Process the main module and its imports
        process_with_imports(str(main_module), project_root)

        # Read and transpile the main module
        with open(main_module, "r") as f:
            dopy_code = f.read()

        processed_code = dopy.preprocess(dopy_code)

        # Create temporary Python file
        temp_path = temp_dir / (main_module.stem + ".py")
        temp_path.write_text(processed_code)

        # Run the processed module
        run_module(str(temp_path))

    # Temporary directory and files are automatically cleaned up
    #


def run_with_files(main_module: Union[str, Path], project_root: Path = None, dopy: Dopy) -> None:
    """
    Run Dopy code while preserving the transpiled Python files in their original directory structure.
    This is used when the --keep flag is passed.

    Args:
        main_module: Path to the main .dopy file to execute
        project_root: Optional root directory for resolving imports
    """
    main_module = Path(main_module)
    if project_root is None:
        project_root = main_module.parent


    # Collect all .dopy files that need to be processed
    collector = DopyImportCollector(project_root)
    all_files = collector.collect_all_imports(main_module)

    # Process each file and save with .py extension
    processed_files = set()
    for dopy_file in all_files:
        # Create output path with .py extension
        output_path = dopy_file.with_suffix(".py")

        # Read and process the file
        with open(dopy_file, "r") as f:
            dopy_code = f.read()

        processed_code = dopy.preprocess(dopy_code)

        # Write processed file
        output_path.write_text(processed_code)
        processed_files.add(output_path)

    # Run the main module
    main_module_py = main_module.with_suffix(".py")
    if main_module_py in processed_files:
        run_module(str(main_module_py))
    else:
        raise ValueError(f"Main module {main_module} was not successfully processed")
