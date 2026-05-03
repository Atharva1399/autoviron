# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [3.0.0] - 2026-05-03

### Added
- **Smart Retry Engine**: Added support to intercept all runtime errors, including `KeyError`.
- **FailureDB**: Introduced `.autoviron_failures.json` to remember past resolutions.
- **Explainer Module**: Added `autoviron explain` command to summarize project architecture.
- **Learning Mode**: Added `autoviron learn <package>` as an offline dictionary.
- **Advanced Dependencies**: Improved AST mapping.
- **Sandbox**: Added `autoviron sandbox` for instant `Dockerfile` generation.

## [2.0.0] - 2026-05-03

### Added
- **Self-Healing Loop**: Automatically installs missing modules on `ImportError`.
- **Plugin Architecture**: Added plugins for FastAPI, Django, and ML detection.
- **Caching**: Added `.autoviron_cache` to skip redundant `pip install` commands.
- **Fix Command**: Added `autoviron fix` to nuke and rebuild environments safely.

### Changed
- Decoupled `detector.py` into a dynamic `plugins/` directory.

## [1.0.0] - 2026-05-03

### Added
- Initial modular rewrite using Typer and Rich.
- ZSH and Bash hooks for auto-activation.
- Basic framework detection.
