from pathlib import Path
from typing import List, Dict

class ProjectHandlerPlugin:
    """Base class for project handler plugins."""
    
    @property
    def name(self) -> str:
        raise NotImplementedError
        
    def detect(self, project_root: Path) -> bool:
        """Return True if this plugin handles the given project."""
        raise NotImplementedError
        
    def get_suggestions(self) -> List[str]:
        """Return a list of AI-like suggestions for this project type."""
        return []
        
    def get_missing_files(self, project_root: Path) -> Dict[str, str]:
        """Return a dict of filename -> content that should be generated."""
        return {}
