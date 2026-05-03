"""
Console UX utilities for AutoViron using Rich.
"""
import sys
from rich.console import Console
from rich.theme import Theme

# Ensure UTF-8 output for emojis on Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except AttributeError:
        pass

# Define a custom theme for AutoViron
autoviron_theme = Theme({
    "info": "dim cyan",
    "warning": "yellow",
    "error": "bold red",
    "success": "bold green",
    "highlight": "bold magenta",
})

# Global console instance
console = Console(theme=autoviron_theme)

def print_welcome():
    """Print the welcome message."""
    console.print("[highlight]AutoViron[/highlight] - Universal Python Environment Launcher", justify="center")
    console.print("=" * 50, justify="center")

def log_info(msg: str):
    """Log an info message."""
    console.print(f"ℹ️ [info]{msg}[/info]")

def log_success(msg: str):
    """Log a success message."""
    console.print(f"✅ [success]{msg}[/success]")

def log_warning(msg: str):
    """Log a warning message."""
    console.print(f"⚠️ [warning]{msg}[/warning]")

def log_error(msg: str):
    """Log an error message."""
    console.print(f"❌ [error]{msg}[/error]")

def print_step(msg: str):
    """Print a step indicator."""
    console.print(f"🚀 [highlight]{msg}[/highlight]")
