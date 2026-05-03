<div align="center">
  <img src="https://img.shields.io/badge/AutoViron-2.0-blueviolet" alt="AutoViron Badge">
  <h1>🚀 AutoViron</h1>
  <p><b>Run any Python script. It fixes itself.</b></p>
</div>

---

Python environments are notoriously painful. You clone a repo, run `python main.py`, and immediately face a wall of `ModuleNotFoundError`s. You set up a `.venv`, run `pip install`, and then your script crashes again because you forgot a `.env` variable. 

**AutoViron** is a self-healing, intelligent developer assistant that ends this cycle. 

It automatically detects your project framework, creates isolated environments, parses your AST for dependencies, catches runtime errors in real-time, injects missing environment variables, and retries your code until it works. It even generates `Dockerfile`s and explains codebases to you.

---

## ✨ The Magic (Demo)

Imagine running a script with missing imports and undefined environment variables:

```bash
$ autoviron run main.py
```

AutoViron's output:
```text
🔍 Detected project type: FastAPI
Found venv environment at /path/to/.venv
Executing: python main.py
⚠️ Smart Retry: Missing module 'bs4' detected.
🧠 Recalled past fix: Auto-installed beautifulsoup4
📦 Auto-installing 'beautifulsoup4'...
✅ Successfully installed 'beautifulsoup4'.
🔄 Retrying execution... (Attempt 1/3)
⚠️ Smart Retry: Missing environment variable 'SECRET_KEY' detected.
💬 Please provide a value for SECRET_KEY: my_super_secret
🔄 Retrying execution... (Attempt 2/3)
✅ Execution Successful!
```

---

## ⚡ Features

* **Self-Healing Execution**: Wraps your Python execution. If it hits an `ImportError`, it automatically maps the module (e.g., `cv2` -> `opencv-python`), installs it, and retries. If it hits a `KeyError`, it prompts you for the missing Env Var, injects it, and retries.
* **Failure Memory**: AutoViron learns from its mistakes. It stores past resolutions in a local `.autoviron_failures.json` database so it never has to ask you the same question twice.
* **Project Explainer**: Clone a massive repo and don't know where to start? Run `autoviron explain` for a plain-English breakdown of the architecture, framework, and entry points.
* **Learning Mode**: Don't know what `uvicorn` does? Run `autoviron learn uvicorn` for an offline dictionary definition.
* **Plugin System**: Built-in support for FastAPI, Django, and Data Science/ML repos.
* **Cloud Sandbox Generator**: Run `autoviron sandbox` to instantly generate a highly optimized `Dockerfile` tailored to your specific framework.
* **Team Sync**: Run `autoviron export` to dump your config to `autoviron.toml` so your whole team shares the exact same setup.

---

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/Atharva1399/autoviron.git
cd autoviron

# Install globally
pip install -e .
```

---

## 🚀 Usage

### 1. The Smart Runner
Just prepend `autoviron run` to any command. It will auto-activate (or create) the `.venv`, install `requirements.txt` (utilizing a super-fast caching engine), and self-heal any runtime errors.
```bash
autoviron run python script.py
```

### 2. The Project Explainer
Understand any codebase in seconds.
```bash
autoviron explain
```

### 3. The Sandbox Generator
Generate an optimized Dockerfile for isolated execution.
```bash
autoviron sandbox
```

### 4. Fix Broken Environments
If your OS updated Python and broke your symlinks, just nuke and pave the environment safely:
```bash
autoviron fix
```

---

## 🏗️ Architecture

* **`core/execution.py`**: The self-healing loop that intercepts `stderr` stack traces.
* **`core/deps.py`**: The AST parser and Smart Dependency Engine mapping dictionaries.
* **`core/failure_db.py`**: The JSON-backed memory storage for retaining error resolutions.
* **`plugins/`**: The extensible project-handler logic for framework-specific behaviors.

## 🥊 Comparison

| Feature | AutoViron | direnv | pipenv |
| :--- | :---: | :---: | :---: |
| Auto-activation on `cd` | ✅ (via `hook`) | ✅ | ❌ |
| Intercepts `ImportError` & auto-installs | ✅ | ❌ | ❌ |
| Intercepts `KeyError` & prompts | ✅ | ❌ | ❌ |
| AI Project Explanation | ✅ | ❌ | ❌ |
| Generates Dockerfiles | ✅ | ❌ | ❌ |

---

## 🤝 Contributing

We welcome contributions! Please see our [CONTRIBUTING.md](CONTRIBUTING.md) for details on how to submit pull requests, run tests, and adhere to our coding standards.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.