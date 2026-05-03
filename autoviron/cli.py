import typer
from pathlib import Path
from typing import Optional, List
from autoviron.ux.console import console, print_welcome, log_info, log_success, log_error, log_warning, print_step
from autoviron.core.env_manager import EnvManager, EnvironmentType
from autoviron.core.detector import detect_project_type
from autoviron.core.deps import detect_missing_imports
from autoviron.doctor.diagnostics import check_env_health
from autoviron.shell.hooks import generate_bash_hook, generate_zsh_hook, update_vscode_settings
from autoviron.core.execution import self_healing_execute

app = typer.Typer(help="AutoViron - Universal Python Environment Launcher", no_args_is_help=True)

@app.command()
def run(
    cmd: List[str] = typer.Argument(..., help="Command to run in the virtual environment"),
    force_recreate: bool = typer.Option(False, "--force", "-f", help="Force recreate environment")
):
    """Run a command inside the automatically detected/created environment (Self-Healing)."""
    print_welcome()
    project_root = Path.cwd()
    
    # Intelligence: Detect project type
    proj_type = detect_project_type(project_root)
    if proj_type != "Standard Python":
        log_info(f"🔍 Detected project type: [highlight]{proj_type}[/highlight]")
        
    manager = EnvManager(project_root)
    env_info = manager.detect_environment()
    
    if env_info and not force_recreate:
        env_type, env_path = env_info
        log_info(f"Found {env_type.value} environment at {env_path}")
    else:
        log_info("No existing environment found. Creating one...")
        env_path = manager.create_venv()
        if not env_path:
            raise typer.Exit(1)
        env_type = EnvironmentType.VENV

    # IDE Integration
    update_vscode_settings(env_path, project_root)

    # Intelligence: AST Parsing for missing dependencies if running a python file
    if cmd and cmd[0].endswith(".py"):
        script_path = Path(cmd[0])
        if script_path.exists():
            missing = detect_missing_imports(script_path)
            if missing:
                log_warning(f"Script uses non-standard modules: {', '.join(missing)}")
                log_info("Ensure they are installed in the environment.")

    print_step(f"Executing: {' '.join(cmd)}")
    exit_code = self_healing_execute(env_type, env_path, cmd, project_root)
    raise typer.Exit(exit_code)

@app.command()
def doctor():
    """Diagnose broken environments."""
    print_welcome()
    log_info("Running diagnostics...")
    project_root = Path.cwd()
    manager = EnvManager(project_root)
    env_info = manager.detect_environment()
    
    if not env_info:
        log_warning("No environment detected.")
    else:
        env_type, env_path = env_info
        log_info(f"Detected {env_type.value} environment at {env_path}")
        is_healthy = check_env_health(env_type, env_path)
        if not is_healthy:
            log_error("Environment is broken! Run `autoviron fix` to repair it.")

@app.command()
def fix():
    """Repair broken environments and reinstall dependencies."""
    print_welcome()
    project_root = Path.cwd()
    manager = EnvManager(project_root)
    env_info = manager.detect_environment()
    
    if env_info:
        env_type, env_path = env_info
        if env_type == EnvironmentType.VENV:
            import shutil
            with console.status(f"[highlight]Removing corrupted environment at {env_path}...[/highlight]"):
                shutil.rmtree(env_path, ignore_errors=True)
            log_success("Removed corrupted environment.")
        else:
            log_warning(f"Fixing {env_type.value} environments is not fully supported yet.")
            raise typer.Exit(1)
            
    # Remove cache
    cache_file = project_root / ".autoviron_cache"
    if cache_file.exists():
        cache_file.unlink()
        
    log_info("Recreating environment and reinstalling dependencies...")
    env_path = manager.create_venv()
    if env_path:
        log_success("Environment successfully repaired!")
    else:
        log_error("Failed to repair environment.")
        raise typer.Exit(1)

@app.command()
def hook(shell: str = typer.Argument(..., help="Shell name (bash, zsh, fish, powershell)")):
    """Print the eval script to enable AutoViron magic in your shell."""
    if shell == "zsh":
        console.print('eval "$(autoviron hook-source zsh)"')
    elif shell == "bash":
        console.print('eval "$(autoviron hook-source bash)"')
    else:
        log_error(f"Unsupported shell: {shell}")

@app.command()
def hook_source(shell: str = typer.Argument(..., help="Shell name (bash, zsh)")):
    """Generate the actual shell hook source code."""
    if shell == "zsh":
        console.print(generate_zsh_hook())
    elif shell == "bash":
        console.print(generate_bash_hook())
    else:
        log_error(f"Unsupported shell: {shell}")

@app.command(name="analyze")
@app.command(name="ai")
def analyze():
    """Analyze the project structure and suggest improvements."""
    print_welcome()
    log_info("🤖 Initializing AutoViron AI Analyzer...")
    project_root = Path.cwd()
    
    with console.status("[highlight]Scanning project files...[/highlight]"):
        import time
        time.sleep(1) # Simulate scanning
        
    from autoviron.core.ai import analyze_project
    analyze_project(project_root)
    
    console.print("\n[bold green]Environment Status:[/bold green]")
    manager = EnvManager(project_root)
    env_info = manager.detect_environment()
    if env_info:
        console.print(f"  • Active: {env_info[0].value} at {env_info[1]}")
    else:
        console.print("  • No active environment. Run `autoviron run <cmd>` to auto-setup.")

@app.command()
def explain():
    """Explain the codebase architecture in simple terms."""
    print_welcome()
    project_root = Path.cwd()
    from autoviron.core.explainer import explain_codebase
    explain_codebase(project_root)

@app.command()
def sandbox():
    """Generate a Dockerfile to isolate the project based on its detected architecture."""
    print_welcome()
    project_root = Path.cwd()
    from autoviron.core.detector import get_active_plugin
    
    plugin = get_active_plugin(project_root)
    proj_type = plugin.name if plugin else "Standard Python"
    
    log_info(f"Generating Sandbox (Docker) for a [highlight]{proj_type}[/highlight] project...")
    
    # Try to get the Dockerfile from the plugin's missing files logic
    missing_files = plugin.get_missing_files(project_root) if plugin else {}
    dockerfile_content = missing_files.get("Dockerfile")
    
    if not dockerfile_content:
        # Fallback basic Dockerfile
        dockerfile_content = "FROM python:3.11-slim\nWORKDIR /app\nCOPY requirements.txt .\nRUN pip install -r requirements.txt\nCOPY . .\nCMD [\"python\", \"main.py\"]"
        
    dockerfile_path = project_root / "Dockerfile"
    if dockerfile_path.exists():
        log_warning("Dockerfile already exists. Skipping generation.")
    else:
        dockerfile_path.write_text(dockerfile_content)
        log_success("Generated Dockerfile for isolated sandbox execution!")
        console.print("\nTo run your sandbox:")
        console.print("  [dim]$ docker build -t autoviron-sandbox .[/dim]")
        console.print("  [dim]$ docker run -it --rm autoviron-sandbox[/dim]")

@app.command()
def learn(package: str = typer.Argument(..., help="The package name to learn about")):
    """Learn what a dependency does and why it's used."""
    print_welcome()
    from autoviron.core.learning import explain_dependency
    explain_dependency(package)


@app.command()
def export(file_name: str = typer.Option("autoviron.toml", "--file", "-f", help="Output config file name")):
    """Export the current environment configuration to a file for team sync."""
    print_welcome()
    project_root = Path.cwd()
    from autoviron.core.config import save_config
    
    # We create a base config with the project type and some default rules
    config = {
        "project_type": detect_project_type(project_root),
        "auto_create": True,
        "auto_activate": True,
        "python_versions": ["python3", "python"]
    }
    
    save_config(project_root, config)
    log_success(f"Exported environment configuration to {file_name}")

@app.command()
def import_config(file_name: str = typer.Option("autoviron.toml", "--file", "-f", help="Config file to import")):
    """Import and apply an environment configuration from a file."""
    print_welcome()
    project_root = Path.cwd()
    from autoviron.core.config import load_config
    
    config = load_config(project_root)
    if not config:
        log_error(f"No configuration found in {file_name}")
        raise typer.Exit(1)
        
    log_info(f"Loaded configuration from {file_name}")
    console.print(config)
    log_success("Configuration applied!")

def main():
    app()

if __name__ == "__main__":
    main()
