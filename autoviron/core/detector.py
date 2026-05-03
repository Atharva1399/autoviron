from pathlib import Path
from typing import Optional
from autoviron.plugins.base import ProjectHandlerPlugin
from autoviron.plugins.builtin import BUILTIN_PLUGINS

def get_active_plugin(project_root: Path) -> Optional[ProjectHandlerPlugin]:
    """Return the first plugin that detects the project."""
    for plugin in BUILTIN_PLUGINS:
        if plugin.detect(project_root):
            return plugin
    return None

def detect_project_type(project_root: Path) -> str:
    """Detects the project type based on plugins."""
    plugin = get_active_plugin(project_root)
    if plugin:
        return plugin.name
    return "Standard Python"
