#!/usr/bin/env python3
"""
Test script for AutoViron functionality.
This script helps verify that AutoViron is working correctly.
"""

import os
import sys
import tempfile
import subprocess
from pathlib import Path

def test_autoviron_import():
    """Test that AutoViron can be imported."""
    try:
        from autoviron import AutoViron
        print("✓ AutoViron import successful")
        return True
    except ImportError as e:
        print(f"✗ AutoViron import failed: {e}")
        return False

def test_config_loading():
    """Test configuration loading."""
    try:
        from autoviron import AutoViron
        autoviron = AutoViron()
        print("✓ Configuration loading successful")
        print(f"  Project root: {autoviron.project_root}")
        return True
    except Exception as e:
        print(f"✗ Configuration loading failed: {e}")
        return False

def test_environment_detection():
    """Test environment detection in a temporary project."""
    try:
        from autoviron import AutoViron
        
        # Create a temporary project directory
        with tempfile.TemporaryDirectory() as temp_dir:
            project_dir = Path(temp_dir) / "test_project"
            project_dir.mkdir()
            
            # Create project indicators
            (project_dir / "requirements.txt").touch()
            (project_dir / ".git").mkdir()
            
            # Create a virtual environment
            venv_dir = project_dir / "venv"
            subprocess.run([sys.executable, "-m", "venv", str(venv_dir)], 
                         check=True, capture_output=True)
            
            # Test environment detection
            original_cwd = os.getcwd()
            os.chdir(project_dir)
            
            try:
                autoviron = AutoViron()
                env_info = autoviron.detect_environment()
                
                if env_info:
                    env_type, env_path = env_info
                    print(f"✓ Environment detection successful")
                    print(f"  Type: {env_type.value}")
                    print(f"  Path: {env_path}")
                    return True
                else:
                    print("✗ Environment detection failed - no environment found")
                    return False
            finally:
                os.chdir(original_cwd)
                
    except Exception as e:
        print(f"✗ Environment detection test failed: {e}")
        return False

def test_shell_integration():
    """Test shell integration scripts."""
    try:
        # Check if shell scripts exist
        script_dir = Path(__file__).parent / "shell"
        scripts = ["bash.sh", "zsh.sh", "fish.fish", "powershell.ps1"]
        
        for script in scripts:
            script_path = script_dir / script
            if script_path.exists():
                print(f"✓ Shell script found: {script}")
            else:
                print(f"✗ Shell script missing: {script}")
                return False
        
        return True
    except Exception as e:
        print(f"✗ Shell integration test failed: {e}")
        return False

def test_config_files():
    """Test configuration files."""
    try:
        # Check if config files exist
        config_dir = Path(__file__).parent / "config"
        config_file = config_dir / "default_config.json"
        
        if config_file.exists():
            print("✓ Default configuration file found")
            
            # Test JSON parsing
            import json
            with open(config_file, 'r') as f:
                config = json.load(f)
            
            required_keys = ["venv_patterns", "python_versions", "auto_create"]
            for key in required_keys:
                if key in config:
                    print(f"  ✓ Config key found: {key}")
                else:
                    print(f"  ✗ Config key missing: {key}")
                    return False
            
            return True
        else:
            print("✗ Default configuration file missing")
            return False
            
    except Exception as e:
        print(f"✗ Configuration test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("AutoViron Test Suite")
    print("=" * 50)
    
    tests = [
        ("Import Test", test_autoviron_import),
        ("Configuration Loading", test_config_loading),
        ("Environment Detection", test_environment_detection),
        ("Shell Integration", test_shell_integration),
        ("Configuration Files", test_config_files),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        print("-" * 30)
        if test_func():
            passed += 1
        else:
            print(f"  Test failed!")
    
    print("\n" + "=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! AutoViron is ready to use.")
        return 0
    else:
        print("❌ Some tests failed. Please check the installation.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 