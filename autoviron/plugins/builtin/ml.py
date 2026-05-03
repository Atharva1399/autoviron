from pathlib import Path
from autoviron.plugins.base import ProjectHandlerPlugin

class MLPlugin(ProjectHandlerPlugin):
    @property
    def name(self) -> str:
        return "Data Science/ML"
        
    def detect(self, project_root: Path) -> bool:
        req_file = project_root / "requirements.txt"
        if req_file.exists():
            content = req_file.read_text().lower()
            if any(p in content for p in ["pandas", "jupyter", "scikit-learn", "tensorflow", "torch"]):
                return True
        
        # Also check for .ipynb files
        if any(project_root.glob("*.ipynb")):
            return True
            
        return False
        
    def get_suggestions(self) -> list:
        return [
            "Use `jupyter lab` instead of `jupyter notebook` for a modern IDE.",
            "Consider tracking datasets with DVC (Data Version Control)."
        ]
        
    def get_missing_files(self, project_root: Path) -> dict:
        files = {}
        if not (project_root / ".gitignore").exists():
            files[".gitignore"] = ".ipynb_checkpoints/\n__pycache__/\ndata/\nmodels/\n.env"
        return files
