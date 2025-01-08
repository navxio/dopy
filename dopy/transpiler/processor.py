from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import os
from typing import Set
from dopy.core import Dopy


class DopyProcessor:
    """Processes multiple .dopy files concurrently"""

    def __init__(self, max_workers: int = None):
        self.max_workers = max_workers or min(32, (os.cpu_count() or 1) + 4)

    def process_file(self, file_path: Path) -> None:
        """Process a single .dopy file"""
        try:
            dopy = Dopy()  # Each thread gets its own instance
            output_path = file_path.with_suffix(".py")
            dopy.process_file(str(file_path), str(output_path))
        except Exception as e:
            print(f"Error processing {file_path}: {e}")

    def process_all(self, files: Set[Path]) -> bool:
        """
        Process all files concurrently.
        Returns True if all files processed successfully, False otherwise.
        """
        failed_files = []

        def process_and_track(file_path: Path):
            try:
                self.process_file(file_path)
            except Exception as e:
                failed_files.append((file_path, str(e)))

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all tasks and wait for completion
            futures = [executor.submit(process_and_track, f) for f in files]
            # Wait for all futures to complete
            for future in futures:
                future.result()  # This will also propagate any exceptions

        if failed_files:
            for file_path, error in failed_files:
                print(f"Failed to process {file_path}: {error}")
            return False

        return True


def process_with_imports(target: str, project_root: Path = None) -> bool:
    """
    Main entry point - collect all imports and process them.
    Returns True if all processing succeeded, False if any failed.
    """
    target_path = Path(target)
    if project_root is None:
        project_root = target_path.parent

    collector = DopyImportCollector(project_root)
    all_files = collector.collect_all_imports(target_path)

    processor = DopyProcessor()
    return processor.process_all(all_files)
