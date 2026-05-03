from pathlib import Path
import json

def load_config(project_root: Path) -> dict:
    """Load configuration from autoviron.toml or autoviron.json."""
    config = {}
    
    # Check for JSON first (legacy)
    json_path = project_root / "autoviron.json"
    if json_path.exists():
        try:
            with open(json_path, "r") as f:
                config.update(json.load(f))
        except json.JSONDecodeError:
            pass
            
    # Check for TOML (preferred)
    toml_path = project_root / "autoviron.toml"
    if toml_path.exists():
        try:
            # Simple TOML parser for basic key-value pairs to avoid heavy dependencies
            content = toml_path.read_text()
            for line in content.splitlines():
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    k = k.strip()
                    v = v.strip().strip('"').strip("'")
                    if v.lower() == "true": v = True
                    elif v.lower() == "false": v = False
                    config[k] = v
        except Exception:
            pass
            
    return config

def save_config(project_root: Path, config: dict):
    """Save configuration to autoviron.toml for team syncing."""
    toml_path = project_root / "autoviron.toml"
    lines = []
    for k, v in config.items():
        if isinstance(v, bool):
            val_str = "true" if v else "false"
        else:
            val_str = f'"{v}"'
        lines.append(f"{k} = {val_str}")
        
    toml_path.write_text("\n".join(lines))
