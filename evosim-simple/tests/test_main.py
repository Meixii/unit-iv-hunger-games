"""
Test module for the main application entry point.
"""

import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.main import main


def test_main_function_exists():
    """Test that the main function exists and is callable."""
    assert callable(main)


def test_main_function_runs():
    """Test that the main function runs without errors."""
    # This test captures stdout to verify the function runs
    import io
    from contextlib import redirect_stdout
    
    f = io.StringIO()
    with redirect_stdout(f):
        main()
    
    output = f.getvalue()
    assert "Evolutionary Simulation" in output
    assert "Phase 1: Infrastructure Setup - COMPLETED" in output


def test_project_structure():
    """Test that the project structure is correctly set up."""
    project_root = Path(__file__).parent.parent
    
    # Check that required directories exist
    assert (project_root / "src").exists()
    assert (project_root / "ui").exists()
    assert (project_root / "analysis").exists()
    assert (project_root / "tests").exists()
    assert (project_root / "config").exists()
    assert (project_root / "docs").exists()
    
    # Check that required files exist
    assert (project_root / "requirements.txt").exists()
    assert (project_root / "setup.py").exists()
    assert (project_root / "pyproject.toml").exists()
    assert (project_root / ".gitignore").exists()
