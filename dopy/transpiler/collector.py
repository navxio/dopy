import ast
from pathlib import Path
from typing import Set, Tuple


class DopyImportCollector:
    def __init__(self, project_root: Path):
        self.project_root = project_root

    def _extract_top_imports(self, content: str) -> Tuple[str, int]:
        """Extract import statements from top of file and return them along with last import line number"""
        lines = content.split("\n")
        import_lines = []
        last_import_line = 0

        for i, line in enumerate(lines):
            stripped = line.strip()
            # Skip empty lines and comments
            if not stripped or stripped.startswith("#"):
                continue

            # If we find a non-import statement, stop processing
            if not (stripped.startswith("import ") or stripped.startswith("from ")):
                break

            # Handle multiline imports that use parentheses
            if "(" in stripped and ")" not in stripped:
                while i < len(lines) and ")" not in lines[i]:
                    import_lines.append(lines[i])
                    i += 1
                if i < len(lines):
                    import_lines.append(lines[i])
                    last_import_line = i
            else:
                import_lines.append(stripped)
                last_import_line = i

        return "\n".join(import_lines), last_import_line

    def _extract_imports(self, file_path: Path) -> Set[Path]:
        """Extract and resolve all potential .dopy imports from file"""
        with open(file_path) as f:
            content = f.read()

        # First extract just the import statements
        import_block, _ = self._extract_top_imports(content)

        imports = set()
        try:
            # Parse just the import statements
            tree = ast.parse(import_block)
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
        except SyntaxError as e:
            print(f"Warning: Syntax error in import statements of {file_path}: {e}")
            # Continue with empty imports set if parsing fails

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
