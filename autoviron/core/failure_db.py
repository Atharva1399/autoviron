import json
from pathlib import Path
from typing import Dict, Any

class FailureDB:
    """Stores past execution failures and their resolutions to avoid repeating mistakes."""
    
    def __init__(self, project_root: Path):
        self.db_path = project_root / ".autoviron_failures.json"
        self._cache = self._load()
        
    def _load(self) -> Dict[str, Any]:
        if self.db_path.exists():
            try:
                return json.loads(self.db_path.read_text())
            except Exception:
                return {}
        return {}
        
    def _save(self):
        try:
            self.db_path.write_text(json.dumps(self._cache, indent=4))
        except Exception:
            pass
            
    def record_failure(self, error_type: str, error_msg: str, resolution: str):
        """Record an error and what was done to fix it."""
        if error_type not in self._cache:
            self._cache[error_type] = []
            
        entry = {"message": error_msg, "resolution": resolution}
        if entry not in self._cache[error_type]:
            self._cache[error_type].append(entry)
            self._save()
            
    def get_resolutions(self, error_type: str) -> list:
        """Get past resolutions for a specific error type."""
        return self._cache.get(error_type, [])
