from pathlib import Path
from autoviron.plugins.base import ProjectHandlerPlugin

class FastAPIPlugin(ProjectHandlerPlugin):
    @property
    def name(self) -> str:
        return "FastAPI"
        
    def detect(self, project_root: Path) -> bool:
        req_file = project_root / "requirements.txt"
        if req_file.exists() and "fastapi" in req_file.read_text().lower():
            return True
        pyproject_file = project_root / "pyproject.toml"
        if pyproject_file.exists() and "fastapi" in pyproject_file.read_text().lower():
            return True
        return False
        
    def get_suggestions(self) -> list:
        return [
            "Consider adding a `docker-compose.yml` for database services.",
            "Use `gunicorn` with `uvicorn` workers for production deployment."
        ]
        
    def get_missing_files(self, project_root: Path) -> dict:
        files = {}
        if not (project_root / ".env").exists():
            files[".env"] = "DATABASE_URL=sqlite:///./test.db\nSECRET_KEY=dev-secret"
        if not (project_root / "Dockerfile").exists():
            files["Dockerfile"] = "FROM python:3.11-slim\nWORKDIR /app\nCOPY requirements.txt .\nRUN pip install -r requirements.txt\nCOPY . .\nCMD [\"uvicorn\", \"main:app\", \"--host\", \"0.0.0.0\", \"--port\", \"8000\"]"
        return files
