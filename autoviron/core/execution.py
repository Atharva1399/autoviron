import sys
import os
import subprocess
import re
from pathlib import Path
from typing import List
import typer
from autoviron.ux.console import console, log_info, log_error, log_warning, log_success
from autoviron.core.env_manager import EnvironmentType
from autoviron.core.deps import get_package_name
from autoviron.core.failure_db import FailureDB

def self_healing_execute(env_type: EnvironmentType, env_path: Path, command: List[str], project_root: Path, max_retries: int = 3) -> int:
    """Execute a command and self-heal by fixing runtime errors dynamically."""
    retries = 0
    failure_db = FailureDB(project_root)
    
    # We only auto-heal for python executions
    is_python_exec = command and command[0] in ("python", "python3") or command[0].endswith(".py")
    
    while retries < max_retries:
        try:
            if env_type == EnvironmentType.POETRY:
                cmd = ["poetry", "run"] + command
                result = subprocess.run(cmd, cwd=project_root, capture_output=True, text=True)
            elif env_type == EnvironmentType.PIPENV:
                cmd = ["pipenv", "run"] + command
                result = subprocess.run(cmd, cwd=project_root, capture_output=True, text=True)
            elif env_type == EnvironmentType.CONDA:
                cmd = ["conda", "run", "-n", env_path.name] + command
                result = subprocess.run(cmd, cwd=project_root, capture_output=True, text=True)
            else:
                python_bin = env_path / ("Scripts" if os.name == "nt" else "bin") / "python"
                cmd = command.copy()
                if cmd[0] in ("python", "python3"):
                    cmd[0] = str(python_bin)
                
                env = os.environ.copy()
                bin_dir = str(env_path / ("Scripts" if os.name == "nt" else "bin"))
                env["PATH"] = f"{bin_dir}{os.pathsep}{env['PATH']}"
                env["VIRTUAL_ENV"] = str(env_path)
                
                result = subprocess.run(cmd, cwd=project_root, capture_output=True, text=True, env=env)
                
            # If successful, print stdout and return
            if result.returncode == 0:
                print(result.stdout, end="")
                return 0
                
            # If failed, analyze stderr for known patterns
            stderr = result.stderr
            
            # 1. Check for ModuleNotFoundError
            mod_match = re.search(r"ModuleNotFoundError: No module named '([^']+)'", stderr)
            if is_python_exec and mod_match:
                missing_module = mod_match.group(1)
                package_name = get_package_name(missing_module)
                log_warning(f"Smart Retry: Missing module '{missing_module}' detected.")
                
                # Check DB for past resolutions
                past_res = failure_db.get_resolutions("ModuleNotFoundError")
                if past_res:
                    log_info(f"🧠 Recalled past fix: {past_res[0]['resolution']}")
                
                if _auto_install_package(env_type, env_path, project_root, package_name):
                    failure_db.record_failure("ModuleNotFoundError", missing_module, f"Auto-installed {package_name}")
                    retries += 1
                    log_info(f"Retrying execution... (Attempt {retries}/{max_retries})")
                    continue
                else:
                    print(result.stdout, end="")
                    print(result.stderr, file=sys.stderr, end="")
                    return result.returncode
                    
            # 2. Check for KeyError (missing env var)
            key_match = re.search(r"KeyError: '([^']+)'", stderr)
            if is_python_exec and key_match:
                missing_var = key_match.group(1)
                log_warning(f"Smart Retry: Missing environment variable '{missing_var}' detected.")
                
                # Interactive prompt for missing variable
                val = typer.prompt(f"Please provide a value for {missing_var}")
                os.environ[missing_var] = val
                
                failure_db.record_failure("KeyError", missing_var, f"Injected ENV var {missing_var}")
                retries += 1
                log_info(f"Retrying execution... (Attempt {retries}/{max_retries})")
                continue

            # Fallback: Not a known error, just print output and return
            if result.stdout:
                print(result.stdout, end="")
            if result.stderr:
                print(result.stderr, file=sys.stderr, end="")
            return result.returncode
                
        except Exception as e:
            log_error(f"Execution error: {e}")
            return 1
            
    log_error("Max smart-retry attempts reached. Aborting.")
    return 1

def _auto_install_package(env_type: EnvironmentType, env_path: Path, project_root: Path, package_name: str) -> bool:
    """Helper to install a package into the correct environment."""
    with console.status(f"[highlight]Auto-installing '{package_name}'...[/highlight]"):
        try:
            if env_type == EnvironmentType.POETRY:
                subprocess.run(["poetry", "add", package_name], cwd=project_root, check=True, capture_output=True)
            elif env_type == EnvironmentType.PIPENV:
                subprocess.run(["pipenv", "install", package_name], cwd=project_root, check=True, capture_output=True)
            elif env_type == EnvironmentType.CONDA:
                subprocess.run(["conda", "install", "-y", "-n", env_path.name, package_name], cwd=project_root, check=True, capture_output=True)
            else:
                pip_bin = env_path / ("Scripts" if os.name == "nt" else "bin") / "pip"
                subprocess.run([str(pip_bin), "install", package_name], cwd=project_root, check=True, capture_output=True)
            log_success(f"Successfully installed '{package_name}'.")
            return True
        except subprocess.CalledProcessError as e:
            log_error(f"Failed to install '{package_name}': {e.stderr if hasattr(e, 'stderr') else e}")
            return False

