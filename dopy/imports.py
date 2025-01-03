import re
import os


class DopyImportHandler:
    """
    Handles recursive transpilation of Dopy imports
    """

    def __init__(self, dopy_processor):
        self.dopy = dopy_processor
        self.processed_files = set()  # Track files we've already processed

    def _extract_imports(self, code):
        """
        Extract potential Dopy imports from code
        Returns list of module names that might be Dopy files
        """
        # Match both 'import module' and 'from module import thing'
        import_pattern = r"^(?:from\s+([.\w]+)\s+import|\s*import\s+([.\w]+))"
        matches = re.finditer(import_pattern, code, re.MULTILINE)

        modules = set()
        for match in matches:
            # Get module name from either 'from' or direct import
            module = match.group(1) or match.group(2)
            # Split in case of multiple imports (import x, y, z)
            for m in module.split(","):
                modules.add(m.strip())
        return modules

    def _find_dopy_file(self, module_name, current_dir):
        """
        Try to find a .dopy file corresponding to the import
        Returns the full path if found, None otherwise
        """
        # Convert module.submodule to module/submodule
        module_path = module_name.replace(".", "/")

        # Places to look for the module
        search_paths = [
            current_dir,
            *os.environ.get("PYTHONPATH", "").split(os.pathsep),
        ]

        for base_path in search_paths:
            # Try both direct .dopy and __init__.dopy in package
            potential_paths = [
                os.path.join(base_path, f"{module_path}.dopy"),
                os.path.join(base_path, module_path, "__init__.dopy"),
            ]

            for path in potential_paths:
                if os.path.exists(path):
                    return path
        return None

    def process_imports(self, file_path, create_py=True):
        """
        Recursively process all Dopy imports in a file

        Args:
            file_path: Path to the main .dopy file
            create_py: If True, creates .py files, otherwise just processes

        Returns:
            List of all processed files
        """
        if file_path in self.processed_files:
            return []

        self.processed_files.add(file_path)
        processed_files = [file_path]

        # Read and process the file
        with open(file_path, "r") as f:
            code = f.read()

        # Find all imports
        current_dir = os.path.dirname(os.path.abspath(file_path))
        imports = self._extract_imports(code)

        # Process each import
        for module_name in imports:
            dopy_file = self._find_dopy_file(module_name, current_dir)
            if dopy_file and dopy_file not in self.processed_files:
                # Recursively process imported file
                processed_files.extend(self.process_imports(dopy_file, create_py))

                if create_py:
                    # Create .py file for the import
                    py_file = dopy_file.rsplit(".", 1)[0] + ".py"
                    self.dopy.process_file(dopy_file, py_file)

        # Process the current file if requested
        if create_py:
            py_file = file_path.rsplit(".", 1)[0] + ".py"
            self.dopy.process_file(file_path, py_file)

        return processed_files


def add_import_handling(dopy_instance):
    """
    Adds import handling capabilities to a Dopy instance
    Returns the import handler
    """
    return DopyImportHandler(dopy_instance)
