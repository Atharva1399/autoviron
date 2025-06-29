# AutoViron

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI version](https://badge.fury.io/py/autoviron.svg)](https://badge.fury.io/py/autoviron)

**AutoViron** is a next-generation universal Python environment launcher that automatically detects and activates the correct virtual environment for any project directory. It goes beyond traditional virtual environment managers by supporting multiple environment types and providing seamless cross-platform integration.

## 🚀 Features

- 🔍 **Universal Environment Detection**: Automatically finds virtual environments, Poetry, Pipenv, Conda, and custom environments
- 🚀 **Auto-Activation**: Seamlessly activates environments when entering project directories
- 🛠️ **Auto-Creation**: Creates new virtual environments when none exist
- 🐚 **Multi-Shell Support**: Works with Bash, Zsh, Fish, and PowerShell
- ⚙️ **Highly Configurable**: Extensive customization through JSON configuration files
- 🔧 **Smart Project Recognition**: Detects projects by common indicators (`.git`, `requirements.txt`, etc.)
- 🎯 **Python Version Management**: Integrates with pyenv and `.python-version` files
- 🔗 **Custom Hooks**: Pre/post activation and creation hooks for extensibility
- 📦 **Package Management**: Optional automatic requirements installation
- 🎯 **Cross-Platform**: Works on Windows, macOS, and Linux
- 📊 **Logging & Debugging**: Built-in logging system for troubleshooting
- ⚡ **Performance**: Caching system for faster environment detection

## 🏗️ Supported Environment Types

- **Standard Virtual Environments**: `venv`, `virtualenv`, `.venv`, `.env`
- **Poetry**: Automatic detection and activation via `poetry shell`
- **Pipenv**: Automatic detection and activation via `pipenv shell`
- **Conda**: Support for Conda environments with `environment.yml`
- **Custom Environments**: User-defined environment patterns

## 📦 Installation

### From Source

```bash
git clone https://github.com/autoviron/autoviron.git
cd autoviron
pip install -e .
```

### From PyPI (when available)

```bash
pip install autoviron
```

## 🚀 Quick Start

### 1. Basic Usage

```bash
# Navigate to a Python project
cd /path/to/your/project

# AutoViron will automatically detect and activate the environment
autoviron

# Or run a command directly in the environment
autoviron python --version
autoviron pip install requests
```

### 2. Shell Integration

#### Bash/Zsh
Add to your `~/.bashrc` or `~/.zshrc`:

```bash
source /path/to/autoviron/shell/bash.sh
# or for zsh
source /path/to/autoviron/shell/zsh.sh
```

#### Fish
Add to your `~/.config/fish/config.fish`:

```fish
source /path/to/autoviron/shell/fish.fish
```

#### PowerShell
Add to your PowerShell profile:

```powershell
. /path/to/autoviron/shell/powershell.ps1
```

### 3. Available Commands

Once integrated, you'll have access to these commands:

- `autoviron_activate` / `autoviron-activate`: Activate environment in current directory
- `autoviron_create` / `autoviron-create`: Create and activate new environment
- `autoviron_deactivate` / `autoviron-deactivate`: Deactivate current environment
- `autoviron_status` / `autoviron-status`: Show current environment status
- `autoviron_run` / `autoviron-run`: Run commands in detected environment

## ⚙️ Configuration

AutoViron supports multiple configuration locations with precedence:

1. `./autovironrc` (project-specific)
2. `./autoviron.json` (project-specific)
3. `~/.autovironrc` (user-specific)
4. `~/.config/autoviron/config.json` (user-specific)
5. `config/default_config.json` (default)

### Example Configuration

```json
{
    "venv_patterns": [
        "venv",
        "env",
        ".venv",
        ".env",
        "virtualenv"
    ],
    "python_versions": [
        "python3",
        "python",
        "python3.11",
        "python3.10"
    ],
    "project_indicators": [
        ".git",
        "pyproject.toml",
        "requirements.txt",
        "setup.py"
    ],
    "auto_create": true,
    "auto_activate": true,
    "shell_integration": true,
    "verbose": false,
    "hooks": {
        "pre_activate": "echo 'Setting up environment...'",
        "post_activate": "echo 'Environment ready!'",
        "pre_create": "echo 'Creating environment...'",
        "post_create": "echo 'Environment created!'"
    },
    "logging": {
        "enabled": false,
        "level": "INFO",
        "file": "~/.autoviron.log"
    }
}
```

## 🔧 Advanced Features

### Custom Hooks

AutoViron supports custom hooks that run before and after environment operations:

```json
{
    "hooks": {
        "pre_activate": "echo 'Pre-activation hook'",
        "post_activate": "pip install -r requirements.txt",
        "pre_create": "echo 'Pre-create hook'",
        "post_create": "echo 'Post-create hook'"
    }
}
```

### Python Version Management

AutoViron integrates with pyenv and `.python-version` files:

```bash
# Create a .python-version file in your project
echo "3.11.0" > .python-version

# AutoViron will use this version when creating environments
autoviron_create
```

### Environment Type Detection

AutoViron automatically detects different environment types:

```bash
# Poetry project
cd poetry-project  # Contains pyproject.toml and poetry.lock
autoviron_activate  # Activates via 'poetry shell'

# Pipenv project  
cd pipenv-project  # Contains Pipfile
autoviron_activate  # Activates via 'pipenv shell'

# Conda project
cd conda-project   # Contains environment.yml
autoviron_activate  # Activates via 'conda activate'

# Standard venv
cd venv-project    # Contains venv/ directory
autoviron_activate  # Activates via 'source venv/bin/activate'
```

## 🎯 Command Line Options

```bash
autoviron [OPTIONS] [COMMAND]

Options:
  -c, --config PATH        Path to configuration file
  -v, --verbose           Enable verbose output
  -q, --quiet             Suppress output
  --no-auto-create        Disable automatic environment creation
  --no-auto-activate      Disable automatic environment activation
  -f, --force             Force operations even if environment exists
  --help                  Show help message

Examples:
  autoviron                    # Auto-detect and activate environment
  autoviron --verbose          # Enable verbose output
  autoviron python --version   # Run command in environment
  autoviron --no-auto-create   # Don't create environment if none exists
  autoviron --config myconfig.json  # Use custom config file
```

## 🏗️ Project Structure

```
autoviron/
├── autoviron.py              # Main AutoViron script
├── shell/                    # Shell integration scripts
│   ├── bash.sh              # Bash integration
│   ├── zsh.sh               # Zsh integration
│   ├── fish.fish            # Fish integration
│   └── powershell.ps1       # PowerShell integration
├── config/                   # Configuration files
│   └── default_config.json  # Default configuration
├── setup.py                 # Package setup
├── requirements.txt         # Dependencies
├── test_autoviron.py       # Test suite
├── .autovironrc.example    # Example configuration
└── README.md               # This file
```

## 📋 Examples

### Poetry Project Workflow

```bash
# Start a new Poetry project
mkdir my-poetry-project
cd my-poetry-project

# Initialize Poetry
poetry init

# AutoViron will detect Poetry and activate the environment
autoviron_activate

# Install dependencies
poetry add requests flask

# Your Poetry environment is now active!
python -c "import requests; print('Success!')"
```

### Multi-Environment Project

```bash
# Project with multiple environment types
cd mixed-project

# AutoViron detects the appropriate environment type
autoviron_status
# Output: Active Poetry environment

# Switch to a different environment
cd ../conda-project
autoviron_activate
# Output: conda activate myenv
```

### Custom Hooks

```bash
# Create a project with custom hooks
mkdir hook-project
cd hook-project

# Create .autovironrc with hooks
cat > .autovironrc << EOF
{
    "hooks": {
        "pre_activate": "echo 'Setting up development environment...'",
        "post_activate": "pip install -r requirements.txt && echo 'Ready!'"
    }
}
EOF

# Activate environment with hooks
autoviron_activate
# Output: 
# Setting up development environment...
# source venv/bin/activate
# Ready!
```

## 🧪 Testing

Run the test suite to verify your installation:

```bash
python test_autoviron.py
```

This will test:
- Import functionality
- Configuration loading
- Environment detection
- Shell integration
- Configuration files

## 🔍 Troubleshooting

### Environment Not Found

1. Check if the environment exists in the expected location
2. Verify the `venv_patterns` in your configuration
3. Use `--verbose` flag for debugging information
4. Check the log file if logging is enabled

### Shell Integration Not Working

1. Ensure the shell script is properly sourced
2. Check file permissions on the shell scripts
3. Verify the path to `autoviron.py` is correct
4. Test with `autoviron_status` command

### Permission Issues

1. Make sure shell scripts are executable: `chmod +x shell/*.sh`
2. Check Python script permissions: `chmod +x autoviron.py`

### Debugging

Enable verbose output and logging:

```bash
# Enable verbose output
autoviron --verbose

# Enable logging in config
{
    "logging": {
        "enabled": true,
        "level": "DEBUG",
        "file": "~/.autoviron.log"
    }
}
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Development Setup

```bash
git clone https://github.com/autoviron/autoviron.git
cd autoviron
pip install -e ".[dev]"
pre-commit install
```

### Running Tests

```bash
pytest
pytest --cov=autoviron
python test_autoviron.py
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Inspired by tools like `auto-venv`, `autovenv`, and `AutoActivator`
- Built with modern Python best practices
- Designed for developer productivity and workflow automation
- Community-driven development and feedback

## 📞 Support

- 📖 [Documentation](https://github.com/autoviron/autoviron#readme)
- 🐛 [Bug Reports](https://github.com/autoviron/autoviron/issues)
- 💡 [Feature Requests](https://github.com/autoviron/autoviron/issues)
- 💬 [Discussions](https://github.com/autoviron/autoviron/discussions)

---

**AutoViron** - Making Python environment management effortless! 🐍✨ 