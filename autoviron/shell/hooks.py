from pathlib import Path
import json

def generate_zsh_hook() -> str:
    """Generate ZSH hook for AutoViron."""
    return """
# AutoViron ZSH Hook
_autoviron_hook() {
    # Only run if there is a venv or similar that we might want to activate
    # For now, we just print a message, but in a real shell script, we'd source the env.
    # A full implementation would check if an env exists, and if so, source it.
    if [ -d ".venv" ]; then
        if [ "$VIRTUAL_ENV" != "$(pwd)/.venv" ]; then
            source .venv/bin/activate
            echo "🚀 AutoViron activated .venv"
        fi
    fi
}

add-zsh-hook chpwd _autoviron_hook
# Run once on initial shell load
_autoviron_hook
"""

def generate_bash_hook() -> str:
    """Generate Bash hook for AutoViron."""
    return """
# AutoViron Bash Hook
_autoviron_hook() {
    if [ -d ".venv" ]; then
        if [ "$VIRTUAL_ENV" != "$(pwd)/.venv" ]; then
            source .venv/bin/activate
            echo "🚀 AutoViron activated .venv"
        fi
    fi
}

PROMPT_COMMAND="_autoviron_hook; $PROMPT_COMMAND"
"""

def update_vscode_settings(env_path: Path, project_root: Path):
    """Update VSCode settings.json to use the AutoViron environment."""
    vscode_dir = project_root / ".vscode"
    vscode_dir.mkdir(exist_ok=True)
    
    settings_file = vscode_dir / "settings.json"
    settings = {}
    
    if settings_file.exists():
        try:
            with open(settings_file, "r") as f:
                settings = json.load(f)
        except json.JSONDecodeError:
            pass
            
    # Assuming standard venv layout for simplicity
    python_path = str(env_path / "bin" / "python")
    import os
    if os.name == "nt":
        python_path = str(env_path / "Scripts" / "python.exe")
        
    settings["python.defaultInterpreterPath"] = python_path
    
    with open(settings_file, "w") as f:
        json.dump(settings, f, indent=4)
