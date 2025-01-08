import ast


class DopyImportCollector:
    """Collects all .dopy files that need to be processed"""

    def __init__(self, project_root: Path):
        self.project_root = project_root

    def _extract_imports(self, file_path: Path) -> Set[Path]:
        """Extract and resolve all potential .dopy imports from file"""
        with open(file_path) as f:
            content = f.read()

        imports = set()
        try:
            tree = ast.parse(content)
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for name in node.names:
                        candidate = self._try_resolve_dopy_path(name.name)
                        if candidate:
                            imports.add(candidate)

                elif isinstance(node, ast.ImportFrom):
                    if node.module:  # Handles 'from x import y'
                        candidate = self._try_resolve_dopy_path(node.module)
                        if candidate:
                            imports.add(candidate)
        except SyntaxError:
            # Skip files with syntax errors - Python will catch them later
            pass

        return imports

    def _try_resolve_dopy_path(self, module_name: str) -> Path:
        """Try to find a .dopy file for this import"""
        # Convert module.submodule to module/submodule.dopy
        parts = module_name.split(".")
        relative_path = Path(*parts)

        # Check project directory
        dopy_path = self.project_root / f"{relative_path}.dopy"
        if dopy_path.exists():
            return dopy_path.resolve()

        return None

    def collect_all_imports(self, entry_point: Path) -> Set[Path]:
        """Get all .dopy files that need to be processed"""
        to_process = {entry_point.resolve()}
        processed = set()

        while to_process:
            current = to_process.pop()
            if current in processed:
                continue

            processed.add(current)
            # Only look for imports in .dopy files
            if current.suffix == ".dopy":
                new_imports = self._extract_imports(current)
                to_process.update(new_imports - processed)

        return processed
