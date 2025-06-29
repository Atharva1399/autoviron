#!/usr/bin/env python3
"""
AutoViron - Universal Python Environment Launcher

Automatically detects and activates the correct virtual environment for any project directory.
Supports multiple virtual environment types and shell integrations.
"""

import os
import sys
import json
import subprocess
import argparse
import logging
from pathlib import Path
from typing import Optional, List, Dict, Any, Tuple
from enum import Enum


class EnvironmentType(Enum):
    """Supported environment types."""
    VENV = "venv"
    VIRTUALENV = "virtualenv"
    CONDA = "conda"
    PIPENV = "pipenv"
    POETRY = "poetry"
    PIPX = "pipx"
    CUSTOM = "custom"


class AutoViron:
    """Main AutoViron class for managing Python virtual environments."""
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize AutoViron with configuration."""
        # Set up a basic logger first
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.CRITICAL)
        self.config = self._load_config(config_path)
        self._setup_logging()
        self.project_root = self._find_project_root()
        
    def _setup_logging(self):
        """Setup logging configuration."""
        if self.config.get("logging", {}).get("enabled", False):
            log_config = self.config["logging"]
            log_file = Path(log_config["file"]).expanduser()
            log_file.parent.mkdir(parents=True, exist_ok=True)
            
            logging.basicConfig(
                level=getattr(logging, log_config.get("level", "INFO")),
                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                handlers=[
                    logging.FileHandler(log_file),
                    logging.StreamHandler() if self.config.get("verbose", False) else logging.NullHandler()
                ]
            )
        else:
            logging.basicConfig(level=logging.CRITICAL)
        
        self.logger = logging.getLogger(__name__)
        
    def _load_config(self, config_path: Optional[str] = None) -> Dict[str, Any]:
        """Load configuration from file or use defaults."""
        if config_path is None:
            # Try multiple config locations
            config_locations = [
                Path.cwd() / ".autovironrc",
                Path.cwd() / "autoviron.json",
                Path.home() / ".autovironrc",
                Path.home() / ".config" / "autoviron" / "config.json",
                Path(__file__).parent / "config" / "default_config.json"
            ]
            
            for location in config_locations:
                if location.exists():
                    config_path = location
                    break
            else:
                config_path = Path(__file__).parent / "config" / "default_config.json"
        
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
                self.logger.info(f"Loaded config from {config_path}")
                return config
        except FileNotFoundError:
            self.logger.warning(f"Config file not found at {config_path}, using defaults")
            return self._get_default_config()
        except json.JSONDecodeError as e:
            self.logger.error(f"Invalid JSON in config file {config_path}: {e}")
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Return default configuration."""
        return {
            "venv_patterns": [
                "venv",
                "env",
                ".venv",
                ".env",
                "virtualenv",
                ".virtualenv"
            ],
            "python_versions": [
                "python3",
                "python",
                "python3.12",
                "python3.11",
                "python3.10",
                "python3.9",
                "python3.8",
                "py"
            ],
            "project_indicators": [
                ".git",
                "pyproject.toml",
                "setup.py",
                "setup.cfg",
                "requirements.txt",
                "requirements-dev.txt",
                "Pipfile",
                "Pipfile.lock",
                "poetry.lock",
                "package.json",
                "package-lock.json",
                "yarn.lock",
                "Cargo.toml",
                "go.mod",
                "composer.json",
                "Gemfile",
                "Rakefile",
                "Makefile",
                "CMakeLists.txt",
                "README.md",
                "README.rst",
                "LICENSE",
                ".gitignore"
            ],
            "auto_create": True,
            "auto_activate": True,
            "shell_integration": True,
            "verbose": False,
            "quiet": False,
            "force": False,
            "python_path": None,
            "venv_name": "venv",
            "pip_upgrade": True,
            "install_requirements": True,
            "requirements_files": [
                "requirements.txt",
                "requirements-dev.txt",
                "dev-requirements.txt"
            ],
            "exclude_patterns": [
                "node_modules",
                ".git",
                "__pycache__",
                "*.pyc",
                ".pytest_cache",
                ".coverage",
                "dist",
                "build",
                "*.egg-info"
            ],
            "shell_commands": {
                "bash": "source",
                "zsh": "source",
                "fish": "source",
                "powershell": "&"
            },
            "hooks": {
                "pre_activate": None,
                "post_activate": None,
                "pre_create": None,
                "post_create": None
            },
            "logging": {
                "enabled": False,
                "level": "INFO",
                "file": "~/.autoviron.log"
            },
            "cache": {
                "enabled": True,
                "ttl": 3600,
                "file": "~/.autoviron_cache.json"
            }
        }
    
    def _find_project_root(self) -> Path:
        """Find the project root directory by looking for common project indicators."""
        current = Path.cwd()
        indicators = self.config.get("project_indicators", [])
        
        while current != current.parent:
            for indicator in indicators:
                if (current / indicator).exists():
                    self.logger.debug(f"Found project root at {current} (indicator: {indicator})")
                    return current
            current = current.parent
        
        self.logger.debug(f"No project indicators found, using current directory: {Path.cwd()}")
        return Path.cwd()
    
    def detect_environment(self) -> Optional[Tuple[EnvironmentType, Path]]:
        """Detect the type and location of the Python environment."""
        # Check for different environment types in order of preference
        
        # 1. Check for Poetry environment
        poetry_env = self._detect_poetry_environment()
        if poetry_env:
            return (EnvironmentType.POETRY, poetry_env)
        
        # 2. Check for Pipenv environment
        pipenv_env = self._detect_pipenv_environment()
        if pipenv_env:
            return (EnvironmentType.PIPENV, pipenv_env)
        
        # 3. Check for Conda environment
        conda_env = self._detect_conda_environment()
        if conda_env:
            return (EnvironmentType.CONDA, conda_env)
        
        # 4. Check for standard virtual environments
        venv_env = self._detect_venv_environment()
        if venv_env:
            return (EnvironmentType.VENV, venv_env)
        
        return None
    
    def _detect_poetry_environment(self) -> Optional[Path]:
        """Detect Poetry virtual environment."""
        poetry_lock = self.project_root / "poetry.lock"
        pyproject_toml = self.project_root / "pyproject.toml"
        
        if poetry_lock.exists() or pyproject_toml.exists():
            try:
                # Try to get Poetry's virtual environment path
                result = subprocess.run(
                    ["poetry", "env", "info", "--path"],
                    cwd=self.project_root,
                    capture_output=True,
                    text=True,
                    check=True
                )
                env_path = Path(result.stdout.strip())
                if env_path.exists():
                    self.logger.debug(f"Found Poetry environment at {env_path}")
                    return env_path
            except (subprocess.CalledProcessError, FileNotFoundError):
                pass
        
        return None
    
    def _detect_pipenv_environment(self) -> Optional[Path]:
        """Detect Pipenv virtual environment."""
        pipfile = self.project_root / "Pipfile"
        
        if pipfile.exists():
            try:
                # Try to get Pipenv's virtual environment path
                result = subprocess.run(
                    ["pipenv", "--venv"],
                    cwd=self.project_root,
                    capture_output=True,
                    text=True,
                    check=True
                )
                env_path = Path(result.stdout.strip())
                if env_path.exists():
                    self.logger.debug(f"Found Pipenv environment at {env_path}")
                    return env_path
            except (subprocess.CalledProcessError, FileNotFoundError):
                pass
        
        return None
    
    def _detect_conda_environment(self) -> Optional[Path]:
        """Detect Conda environment."""
        environment_yml = self.project_root / "environment.yml"
        
        if environment_yml.exists():
            # Look for conda environment in common locations
            conda_envs = [
                self.project_root / ".conda",
                self.project_root / "env",
                Path.home() / ".conda" / "envs" / self.project_root.name
            ]
            
            for env_path in conda_envs:
                if env_path.exists() and self._is_valid_conda_env(env_path):
                    self.logger.debug(f"Found Conda environment at {env_path}")
                    return env_path
        
        return None
    
    def _is_valid_conda_env(self, env_path: Path) -> bool:
        """Check if a directory is a valid Conda environment."""
        conda_indicators = ["bin", "Scripts", "conda-meta"]
        return any((env_path / indicator).exists() for indicator in conda_indicators)
    
    def _detect_venv_environment(self) -> Optional[Path]:
        """Detect standard virtual environment."""
        for pattern in self.config["venv_patterns"]:
            venv_path = self.project_root / pattern
            if venv_path.exists() and self._is_valid_venv(venv_path):
                self.logger.debug(f"Found virtual environment at {venv_path}")
                return venv_path
        
        return None
    
    def _is_valid_venv(self, venv_path: Path) -> bool:
        """Check if a directory is a valid virtual environment."""
        indicators = [
            "Scripts" if os.name == "nt" else "bin",
            "Lib",
            "pyvenv.cfg"
        ]
        
        return any((venv_path / indicator).exists() for indicator in indicators)
    
    def _get_python_version(self) -> Optional[str]:
        """Get Python version from .python-version file or pyenv."""
        python_version_file = self.project_root / ".python-version"
        
        if python_version_file.exists():
            try:
                with open(python_version_file, 'r') as f:
                    version = f.read().strip()
                    self.logger.debug(f"Found Python version {version} in .python-version")
                    return version
            except Exception as e:
                self.logger.warning(f"Error reading .python-version: {e}")
        
        return None
    
    def _run_hook(self, hook_name: str) -> bool:
        """Run a custom hook if configured."""
        hooks = self.config.get("hooks", {})
        hook_script = hooks.get(hook_name)
        
        if hook_script:
            try:
                self.logger.debug(f"Running hook: {hook_name}")
                result = subprocess.run(
                    hook_script,
                    shell=True,
                    cwd=self.project_root,
                    capture_output=True,
                    text=True
                )
                if result.returncode != 0:
                    self.logger.warning(f"Hook {hook_name} failed: {result.stderr}")
                    return False
                return True
            except Exception as e:
                self.logger.error(f"Error running hook {hook_name}: {e}")
                return False
        
        return True
    
    def create_venv(self, python_version: Optional[str] = None) -> Optional[Path]:
        """Create a new virtual environment."""
        if not self.config["auto_create"]:
            return None
        
        # Run pre-create hook
        if not self._run_hook("pre_create"):
            return None
        
        if python_version is None:
            python_version = self._get_python_version() or self._find_available_python()
        
        if not python_version:
            print("Error: No suitable Python version found")
            return None
        
        venv_name = self.config.get("venv_name", "venv")
        venv_path = self.project_root / venv_name
        
        try:
            subprocess.run([
                python_version, "-m", "venv", str(venv_path)
            ], check=True, capture_output=True)
            
            print(f"Created virtual environment: {venv_path}")
            
            # Run post-create hook
            self._run_hook("post_create")
            
            return venv_path
        except subprocess.CalledProcessError as e:
            print(f"Error creating virtual environment: {e}")
            return None
    
    def _find_available_python(self) -> Optional[str]:
        """Find an available Python version."""
        for version in self.config["python_versions"]:
            try:
                subprocess.run([version, "--version"], 
                             check=True, capture_output=True)
                return version
            except (subprocess.CalledProcessError, FileNotFoundError):
                continue
        return None
    
    def activate_environment(self, env_type: EnvironmentType, env_path: Path) -> bool:
        """Generate activation command for the environment."""
        if not self.config["auto_activate"]:
            return False
        
        # Run pre-activate hook
        if not self._run_hook("pre_activate"):
            return False
        
        activation_command = self._get_activation_command(env_type, env_path)
        
        if activation_command:
            # Print activation command for shell integration
            if self.config["shell_integration"]:
                print(activation_command)
            
            # Run post-activate hook
            self._run_hook("post_activate")
            return True
        
        return False
    
    def _get_activation_command(self, env_type: EnvironmentType, env_path: Path) -> Optional[str]:
        """Get the appropriate activation command for the environment type."""
        if env_type == EnvironmentType.POETRY:
            return f"poetry shell"
        
        elif env_type == EnvironmentType.PIPENV:
            return f"pipenv shell"
        
        elif env_type == EnvironmentType.CONDA:
            return f"conda activate {env_path.name}"
        
        elif env_type == EnvironmentType.VENV:
            if os.name == "nt":  # Windows
                activate_script = env_path / "Scripts" / "activate"
            else:  # Unix-like
                activate_script = env_path / "bin" / "activate"
            
            if activate_script.exists():
                return f"source {activate_script}"
            else:
                self.logger.error(f"Activation script not found at {activate_script}")
                return None
        
        return None
    
    def run(self, command: Optional[List[str]] = None) -> int:
        """Main entry point for AutoViron."""
        if self.config["verbose"]:
            print(f"Project root: {self.project_root}")
        
        # Detect environment
        env_info = self.detect_environment()
        
        if env_info:
            env_type, env_path = env_info
            if self.config["verbose"]:
                print(f"Found {env_type.value} environment: {env_path}")
            
            if self.config["auto_activate"]:
                self.activate_environment(env_type, env_path)
            
            # Execute command in environment if provided
            if command:
                return self._execute_in_environment(env_type, env_path, command)
        else:
            if self.config["verbose"]:
                print("No environment found")
            
            # Create new virtual environment if auto_create is enabled
            if self.config["auto_create"]:
                env_path = self.create_venv()
                if env_path and self.config["auto_activate"]:
                    self.activate_environment(EnvironmentType.VENV, env_path)
        
        return 0
    
    def _execute_in_environment(self, env_type: EnvironmentType, env_path: Path, command: List[str]) -> int:
        """Execute a command within the environment."""
        try:
            if env_type == EnvironmentType.POETRY:
                result = subprocess.run(["poetry", "run"] + command, cwd=self.project_root)
            elif env_type == EnvironmentType.PIPENV:
                result = subprocess.run(["pipenv", "run"] + command, cwd=self.project_root)
            elif env_type == EnvironmentType.CONDA:
                result = subprocess.run(["conda", "run", "-n", env_path.name] + command)
            else:  # VENV
                if os.name == "nt":  # Windows
                    python_path = env_path / "Scripts" / "python.exe"
                else:  # Unix-like
                    python_path = env_path / "bin" / "python"
                
                result = subprocess.run([str(python_path)] + command)
            
            return result.returncode
        except Exception as e:
            print(f"Error executing command: {e}")
            return 1


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="AutoViron - Universal Python Environment Launcher"
    )
    parser.add_argument(
        "--config", "-c",
        help="Path to configuration file"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output"
    )
    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="Suppress output"
    )
    parser.add_argument(
        "--no-auto-create",
        action="store_true",
        help="Disable automatic virtual environment creation"
    )
    parser.add_argument(
        "--no-auto-activate",
        action="store_true",
        help="Disable automatic virtual environment activation"
    )
    parser.add_argument(
        "--force", "-f",
        action="store_true",
        help="Force operations even if environment exists"
    )
    parser.add_argument(
        "command",
        nargs="*",
        help="Command to execute in the virtual environment"
    )
    
    args = parser.parse_args()
    
    # Initialize AutoViron
    autoviron = AutoViron(args.config)
    
    # Override config with command line arguments
    if args.verbose:
        autoviron.config["verbose"] = True
    if args.quiet:
        autoviron.config["quiet"] = True
    if args.no_auto_create:
        autoviron.config["auto_create"] = False
    if args.no_auto_activate:
        autoviron.config["auto_activate"] = False
    if args.force:
        autoviron.config["force"] = True
    
    # Run AutoViron
    return autoviron.run(args.command if args.command else None)


if __name__ == "__main__":
    sys.exit(main()) 