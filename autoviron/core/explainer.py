from pathlib import Path
from autoviron.core.detector import get_active_plugin
from autoviron.ux.console import console

def explain_codebase(project_root: Path):
    """Explain the architecture of the codebase in simple terms."""
    plugin = get_active_plugin(project_root)
    
    console.print(f"\n[bold magenta]Codebase Explanation[/bold magenta]")
    console.print("-" * 50)
    
    if plugin:
        console.print(f"This is a [bold]{plugin.name}[/bold] project.")
        if plugin.name == "FastAPI":
            console.print("It uses an ASGI architecture to serve high-performance async APIs.")
            console.print("Typical entry point is a file running `uvicorn` or containing a `FastAPI()` instance.")
        elif plugin.name == "Django":
            console.print("It follows the Model-View-Template (MVT) pattern for web development.")
            console.print("The `manage.py` file is the primary entry point for commands.")
        elif plugin.name == "Data Science/ML":
            console.print("It focuses on data analysis or machine learning modeling.")
            console.print("You likely have Jupyter notebooks (`.ipynb`) or scripts utilizing pandas/scikit-learn.")
    else:
        console.print("This is a standard Python application.")
        console.print("It likely relies on standard `python script.py` execution.")
        
    console.print("\n[bold cyan]Project Structure Summary:[/bold cyan]")
    # Basic directory parsing heuristic
    dirs = [d.name for d in project_root.iterdir() if d.is_dir() and not d.name.startswith(".")]
    files = [f.name for f in project_root.iterdir() if f.is_file() and not f.name.startswith(".")]
    
    console.print(f"  • Top-level directories: {', '.join(dirs) if dirs else 'None'}")
    
    if "requirements.txt" in files:
        console.print("  • Dependencies are managed via `requirements.txt`.")
    elif "pyproject.toml" in files:
        console.print("  • Dependencies and tooling are managed via `pyproject.toml`.")
        
    if "tests" in dirs or "test" in dirs:
        console.print("  • Testing framework is present.")
    
    console.print("\nTo dive into specific dependencies, run `autoviron learn <package>`.")
