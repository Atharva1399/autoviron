from pathlib import Path
from autoviron.plugins.base import ProjectHandlerPlugin

class DjangoPlugin(ProjectHandlerPlugin):
    @property
    def name(self) -> str:
        return "Django"
        
    def detect(self, project_root: Path) -> bool:
        if (project_root / "manage.py").exists():
            return True
        req_file = project_root / "requirements.txt"
        if req_file.exists() and "django" in req_file.read_text().lower():
            return True
        return False
        
    def get_suggestions(self) -> list:
        return [
            "Consider separating `settings.py` into `base.py`, `dev.py`, and `prod.py`.",
            "Ensure `DEBUG = False` in production."
        ]
        
    def get_missing_files(self, project_root: Path) -> dict:
        files = {}
        if not (project_root / ".env").exists():
            files[".env"] = "DJANGO_SECRET_KEY=dev-secret-key\nDEBUG=True"
        return files
