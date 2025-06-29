#!/usr/bin/env python3
"""
Setup script for AutoViron - Universal Python Environment Launcher
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), "README.md")
    if os.path.exists(readme_path):
        with open(readme_path, "r", encoding="utf-8") as f:
            return f.read()
    return "AutoViron - Universal Python Environment Launcher"

# Read requirements
def read_requirements():
    requirements_path = os.path.join(os.path.dirname(__file__), "requirements.txt")
    if os.path.exists(requirements_path):
        with open(requirements_path, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip() and not line.startswith("#")]
    return []

setup(
    name="autoviron",
    version="1.0.0",
    author="AutoViron Contributors",
    author_email="autoviron@protonmail.com",
    description="Universal Python Environment Launcher",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/Atharva1399/autoviron",
    project_urls={
        "Bug Reports": "https://github.com/Atharva1399/autoviron/issues",
        "Source": "https://github.com/Atharva1399/autoviron",
        "Documentation": "https://github.com/Atharva1399/autoviron#readme",
    },
    packages=find_packages(),
    py_modules=["autoviron"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Systems Administration",
        "Topic :: Utilities",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.8",
            "mypy>=0.800",
            "pre-commit>=2.0",
        ],
        "test": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "pytest-mock>=3.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "autoviron=autoviron:main",
        ],
    },
    include_package_data=True,
    package_data={
        "autoviron": [
            "config/*.json",
            "shell/*.sh",
            "shell/*.fish",
            "shell/*.ps1",
        ],
    },
    data_files=[
        ("config", ["config/default_config.json"]),
        ("shell", [
            "shell/bash.sh",
            "shell/zsh.sh", 
            "shell/fish.fish",
            "shell/powershell.ps1"
        ]),
    ],
    keywords="python virtual environment venv automation development tools",
    license="MIT",
    zip_safe=False,
) 