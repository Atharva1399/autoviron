import os
import sys
import subprocess
from pathlib import Path
from typing import Optional, Tuple, List, Dict, Any
from enum import Enum
from autoviron.ux.console import log_info, log_success, log_error, console

class EnvironmentType(Enum):
    VENV = "venv"
    CONDA = "conda"
    PIPENV = "pipenv"
    POETRY = "poetry"
    CUSTOM = "custom"

class EnvManager:
    def __init__(self, project_root: Path):
        self.project_root = project_root
        # Try to load config or use defaults
        self.python_versions = ["python3", "python", "python3.12", "python3.11", "python3.10", "py"]
        self.venv_patterns = ["venv", "env", ".venv", ".env"]

    def detect_environment(self) -> Optional[Tuple[EnvironmentType, Path]]:
        """Detect the type and location of the Python environment."""
        poetry_env = self._detect_poetry()
        if poetry_env: return (EnvironmentType.POETRY, poetry_env)

        pipenv_env = self._detect_pipenv()
        if pipenv_env: return (EnvironmentType.PIPENV, pipenv_env)

        conda_env = self._detect_conda()
        if conda_env: return (EnvironmentType.CONDA, conda_env)

        venv_env = self._detect_venv()
        if venv_env: return (EnvironmentType.VENV, venv_env)

        return None

    def _detect_poetry(self) -> Optional[Path]:
        if (self.project_root / "poetry.lock").exists() or (self.project_root / "pyproject.toml").exists():
            try:
                result = subprocess.run(["poetry", "env", "info", "--path"], cwd=self.project_root, capture_output=True, text=True)
                if result.returncode == 0:
                    env_path = Path(result.stdout.strip())
                    if env_path.exists(): return env_path
            except FileNotFoundError: pass
        return None

    def _detect_pipenv(self) -> Optional[Path]:
        if (self.project_root / "Pipfile").exists():
            try:
                result = subprocess.run(["pipenv", "--venv"], cwd=self.project_root, capture_output=True, text=True)
                if result.returncode == 0:
                    env_path = Path(result.stdout.strip())
                    if env_path.exists(): return env_path
            except FileNotFoundError: pass
        return None

    def _detect_conda(self) -> Optional[Path]:
        if (self.project_root / "environment.yml").exists():
            conda_envs = [self.project_root / ".conda", self.project_root / "env", Path.home() / ".conda" / "envs" / self.project_root.name]
            for env in conda_envs:
                if env.exists() and any((env / ind).exists() for ind in ["bin", "Scripts"]): return env
        return None

    def _detect_venv(self) -> Optional[Path]:
        for pattern in self.venv_patterns:
            venv_path = self.project_root / pattern
            if venv_path.exists() and any((venv_path / ind).exists() for ind in ["bin", "Scripts", "pyvenv.cfg"]):
                return venv_path
        return None

    def create_venv(self) -> Optional[Path]:
        python_cmd = self._find_python()
        if not python_cmd:
            log_error("Could not find a suitable Python installation.")
            return None
        
        venv_path = self.project_root / ".venv"
        with console.status("[highlight]Creating virtual environment...[/highlight]"):
            try:
                subprocess.run([python_cmd, "-m", "venv", str(venv_path)], check=True, capture_output=True)
                log_success(f"Virtual environment created at {venv_path}")
            except subprocess.CalledProcessError as e:
                log_error(f"Failed to create venv: {e}")
                return None
                
        # Auto-install deps
        self._auto_install_deps(venv_path)
        return venv_path

    def _auto_install_deps(self, venv_path: Path):
        req_file = self.project_root / "requirements.txt"
        if req_file.exists():
            import hashlib
            cache_file = self.project_root / ".autoviron_cache"
            current_hash = hashlib.md5(req_file.read_bytes()).hexdigest()
            
            if cache_file.exists():
                try:
                    import json
                    cache = json.loads(cache_file.read_text())
                    if cache.get("req_hash") == current_hash:
                        log_info("Dependencies unchanged. Skipping reinstall.")
                        return
                except Exception:
                    pass
                    
            pip_bin = venv_path / ("Scripts" if os.name == "nt" else "bin") / "pip"
            with console.status("[highlight]Installing dependencies from requirements.txt...[/highlight]"):
                subprocess.run([str(pip_bin), "install", "-r", "requirements.txt"], cwd=self.project_root, capture_output=True)
                log_success("Dependencies installed.")
                
            try:
                import json
                cache_file.write_text(json.dumps({"req_hash": current_hash}))
            except Exception:
                pass

    def _find_python(self) -> Optional[str]:
        for py in self.python_versions:
            try:
                if subprocess.run([py, "--version"], capture_output=True).returncode == 0:
                    return py
            except FileNotFoundError: continue
        return None

    def get_activation_command(self, env_type: EnvironmentType, env_path: Path) -> Optional[str]:
        if env_type == EnvironmentType.POETRY: return "poetry shell"
        elif env_type == EnvironmentType.PIPENV: return "pipenv shell"
        elif env_type == EnvironmentType.CONDA: return f"conda activate {env_path.name}"
        elif env_type == EnvironmentType.VENV:
            activate_script = env_path / ("Scripts" if os.name == "nt" else "bin") / "activate"
            if activate_script.exists():
                return f"source {activate_script}"
        return None

    def execute_in_env(self, env_type: EnvironmentType, env_path: Path, command: List[str]) -> int:
        try:
            if env_type == EnvironmentType.POETRY:
                return subprocess.run(["poetry", "run"] + command, cwd=self.project_root).returncode
            elif env_type == EnvironmentType.PIPENV:
                return subprocess.run(["pipenv", "run"] + command, cwd=self.project_root).returncode
            elif env_type == EnvironmentType.CONDA:
                return subprocess.run(["conda", "run", "-n", env_path.name] + command, cwd=self.project_root).returncode
            else:
                python_bin = env_path / ("Scripts" if os.name == "nt" else "bin") / "python"
                if command[0] == "python":
                    command[0] = str(python_bin)
                # If command is something else like pytest, we'd need to find it in the bin dir, 
                # but for now we execute the command as is, assuming it will run via python -m or similar, 
                # or we just prepend the bin dir to PATH.
                env = os.environ.copy()
                bin_dir = str(env_path / ("Scripts" if os.name == "nt" else "bin"))
                env["PATH"] = f"{bin_dir}{os.pathsep}{env['PATH']}"
                env["VIRTUAL_ENV"] = str(env_path)
                return subprocess.run(command, cwd=self.project_root, env=env).returncode
        except Exception as e:
            log_error(f"Error executing command: {e}")
            return 1
