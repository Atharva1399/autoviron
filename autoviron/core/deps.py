import ast
import pkgutil
from pathlib import Path
from typing import List, Set
from autoviron.ux.console import log_info, log_warning, console

# Mapping of common import names to their PyPI package names
IMPORT_TO_PACKAGE = {
    "yaml": "pyyaml",
    "bs4": "beautifulsoup4",
    "PIL": "Pillow",
    "cv2": "opencv-python",
    "sklearn": "scikit-learn",
    "dotenv": "python-dotenv",
    "jwt": "PyJWT",
    "dateutil": "python-dateutil",
    "redis": "redis",
    "psycopg2": "psycopg2-binary",
    "git": "GitPython",
    "msgpack": "msgpack",
    "flask_sqlalchemy": "Flask-SQLAlchemy",
    "sqlalchemy": "SQLAlchemy",
    "pydantic": "pydantic",
    "pydantic_settings": "pydantic-settings",
    "fastapi": "fastapi",
    "uvicorn": "uvicorn",
    "discord": "discord.py",
    "boto3": "boto3",
}

def get_package_name(import_name: str) -> str:
    """Map an import name to its PyPI package name."""
    return IMPORT_TO_PACKAGE.get(import_name, import_name)

def get_stdlib_modules() -> Set[str]:
    """Return a set of standard library module names."""
    try:
        import sys
        return set(sys.stdlib_module_names)
    except AttributeError:
        return {m.name for m in pkgutil.iter_modules()}

def detect_missing_imports(file_path: Path) -> List[str]:
    """Scan a Python file for imports that might be missing."""
    if not file_path.exists() or file_path.suffix != ".py":
        return []

    try:
        content = file_path.read_text()
        tree = ast.parse(content)
    except SyntaxError:
        log_warning(f"Syntax error in {file_path}, skipping dependency detection.")
        return []

    imported_modules = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imported_modules.add(alias.name.split('.')[0])
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imported_modules.add(node.module.split('.')[0])

    stdlib = get_stdlib_modules()
    missing_candidates = []
    for mod in imported_modules:
        if mod not in stdlib:
            missing_candidates.append(get_package_name(mod))

    return missing_candidates
