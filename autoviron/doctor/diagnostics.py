from pathlib import Path
from autoviron.core.env_manager import EnvironmentType
from autoviron.ux.console import log_info, log_error, log_warning, log_success

def check_env_health(env_type: EnvironmentType, env_path: Path) -> bool:
    """Check if the environment is healthy."""
    is_healthy = True
    
    if not env_path.exists():
        log_error(f"Environment path {env_path} does not exist.")
        return False
        
    if env_type == EnvironmentType.VENV:
        # Check if python executable exists
        import os
        python_bin = env_path / ("Scripts" if os.name == "nt" else "bin") / ("python.exe" if os.name == "nt" else "python")
        if not python_bin.exists():
            log_error(f"Python executable missing in venv: {python_bin}")
            is_healthy = False
            
        # Check if the python executable is a broken symlink (on Unix)
        if os.name != "nt":
            if python_bin.is_symlink() and not python_bin.resolve().exists():
                log_error(f"Python executable is a broken symlink: {python_bin}")
                is_healthy = False
                
    if is_healthy:
        log_success("Environment passed health checks.")
        
    return is_healthy
