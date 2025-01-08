from pathlib import Path
from .collector import DopyImportCollector
from .processor import DopyProcessor


def process_with_imports(target: str, project_root: Path = None) -> bool:
    """Main entry point for transpilation with imports"""
    target_path = Path(target)
    if project_root is None:
        project_root = target_path.parent

    collector = DopyImportCollector(project_root)
    all_files = collector.collect_all_imports(target_path)

    processor = DopyProcessor()
    return processor.process_all(all_files)
