from pathlib import Path
import tempfile
import importlib.util
import sys
import shutil
from typing import Union

from dopy.transpiler import process_with_imports
from dopy.transpiler.collector import DopyImportCollector
from dopy.transpiler.processor import DopyProcessor


def setup_module_path(module_path: Union[str, Path]) -> tuple[str, Path]:
    """Set up the Python path for module imports and return the module name and parent path."""
    module_path = Path(module_path).resolve()
    module_parent = module_path.parent
    module_name = module_path.stem

    # Add both the parent directory and project root to sys.path
    parent_str = str(module_parent)
    root_str = str(module_parent.parent)  # Add parent of parent for package imports

    # Insert both paths at the beginning of sys.path
    if root_str not in sys.path:
        sys.path.insert(0, root_str)
    if parent_str not in sys.path:
        sys.path.insert(0, parent_str)

    return module_name, module_parent


def run_module(module_path: str):
    """Run a Python module dynamically from a file path."""
    module_name, parent_path = setup_module_path(module_path)

    # Create and load the module spec with the full file path
    full_path = str(Path(module_path).resolve())
    spec = importlib.util.spec_from_file_location(
        "__main__", full_path
    )  # Changed module_name to "__main__"
    if spec is None:
        raise ImportError(f"Could not load module spec for {module_path}")

    module = importlib.util.module_from_spec(spec)

    # Add both the base module and the full path to sys.modules
    sys.modules["__main__"] = module  # Changed to use "__main__"

    # Execute the module
    if spec.loader is None:
        raise ImportError(f"Could not load module {module_path}")

    spec.loader.exec_module(module)


def run_with_files(main_module: Union[str, Path], project_root: Path = None) -> None:
    """Run Dopy code while preserving the transpiled Python files."""
    main_module = Path(main_module)
    if project_root is None:
        project_root = main_module.parent

    # Process all files
    success = process_with_imports(str(main_module), project_root)
    if not success:
        raise ValueError(f"Failed to process {main_module} and its dependencies")

    # Run the processed module
    main_module_py = main_module.with_suffix(".py")
    if main_module_py.exists():
        run_module(str(main_module_py))
    else:
        raise ValueError(f"Main module {main_module} was not successfully processed")


def run_without_files(main_module: Union[str, Path], project_root: Path = None) -> None:
    """Run Dopy code using a temporary directory."""
    main_module = Path(main_module)
    if project_root is None:
        project_root = main_module.parent

    # Create temporary directory
    temp_dir = None
    try:
        temp_dir = Path(tempfile.mkdtemp())

        # Collect all dependencies
        collector = DopyImportCollector(project_root)
        all_files = collector.collect_all_imports(main_module)

        # Copy files to temp directory preserving structure
        temp_files = set()
        for file_path in all_files:
            rel_path = file_path.relative_to(project_root)
            temp_path = temp_dir / rel_path
            temp_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(file_path, temp_path)
            temp_files.add(temp_path)

        # Process all files
        processor = DopyProcessor()
        if not processor.process_all(temp_files):
            raise ValueError("Failed to process one or more files")

        # Run the processed module
        temp_main = temp_dir / main_module.relative_to(project_root)
        temp_main_py = temp_main.with_suffix(".py")
        if temp_main_py.exists():
            run_module(str(temp_main_py))
        else:
            raise ValueError(f"Main module {temp_main} was not successfully processed")

    finally:
        if temp_dir and temp_dir.exists():
            shutil.rmtree(temp_dir)
