from pathlib import Path
from autoviron.core.detector import get_active_plugin
from autoviron.ux.console import console, log_info, log_success
import typer

def analyze_project(project_root: Path):
    """Analyze the project and provide AI-like suggestions and file generation."""
    plugin = get_active_plugin(project_root)
    proj_type = plugin.name if plugin else "Standard Python"
    
    console.print(f"\n[bold magenta]AI Project Analysis[/bold magenta]")
    console.print("-" * 50)
    console.print(f"📁 [bold]Root:[/bold] {project_root}")
    console.print(f"🏗️  [bold]Type:[/bold] {proj_type}")
    
    console.print("\n[bold cyan]💡 Suggestions:[/bold cyan]")
    suggestions = plugin.get_suggestions() if plugin else []
    if not suggestions:
        suggestions = [
            "Consider adding a `pyproject.toml` or `requirements.txt`.",
            "Add a `.gitignore` tailored for Python."
        ]
        
    for s in suggestions:
        console.print(f"  • {s}")
        
    # Check for missing files
    missing_files = plugin.get_missing_files(project_root) if plugin else {}
    if missing_files:
        console.print("\n[bold yellow]🛠️  Missing Files Detected:[/bold yellow]")
        for filename in missing_files.keys():
            console.print(f"  • {filename}")
            
        generate = typer.confirm("\nWould you like AutoViron to generate these files?")
        if generate:
            for filename, content in missing_files.items():
                filepath = project_root / filename
                filepath.write_text(content)
                log_success(f"Generated {filename}")
    else:
        console.print("\n[bold green]✅ No critical files are missing.[/bold green]")
