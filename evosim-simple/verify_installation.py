#!/usr/bin/env python3
"""
Installation Verification Script for Modern GUI

This script verifies that all dependencies are properly installed
and the modern GUI can be launched successfully.
"""

import sys
import os

def check_python_version():
    """Check if Python version is compatible."""
    version = sys.version_info
    if version.major == 3 and version.minor >= 8:
        print(f"[SUCCESS] Python {version.major}.{version.minor}.{version.micro} is compatible")
        return True
    else:
        print(f"[ERROR] Python {version.major}.{version.minor}.{version.micro} is not compatible")
        print("Arcade requires Python 3.8 or higher")
        return False

def check_dependencies():
    """Check if all required dependencies are installed."""
    dependencies = [
        ('arcade', 'Arcade library for 2D graphics'),
        ('numpy', 'NumPy for numerical computations'),
        ('matplotlib', 'Matplotlib for plotting'),
    ]
    
    all_installed = True
    
    for module, description in dependencies:
        try:
            __import__(module)
            print(f"[SUCCESS] {description} is installed")
        except ImportError:
            print(f"[ERROR] {description} is NOT installed")
            print(f"   Install with: pip install {module}")
            all_installed = False
    
    return all_installed

def check_simulation_imports():
    """Check if simulation modules can be imported."""
    try:
        # Add current directory to path
        sys.path.insert(0, '.')
        
        # Test imports
        from src.simulation import Simulation
        from src.animal import Animal
        from src.environment import GridWorld
        from src.neural_network import NeuralNetwork
        
        print("[SUCCESS] All simulation modules can be imported")
        return True
        
    except ImportError as e:
        print(f"[ERROR] Failed to import simulation modules: {e}")
        print("Make sure you're running this from the project root directory")
        return False

def check_modern_gui():
    """Check if modern GUI can be imported."""
    try:
        from ui.modern_gui import ModernSimulationGUI
        print("[SUCCESS] Modern GUI can be imported")
        return True
        
    except ImportError as e:
        print(f"[ERROR] Failed to import modern GUI: {e}")
        return False

def main():
    """Main verification function."""
    print("=" * 60)
    print("INSTALLATION VERIFICATION FOR MODERN GUI")
    print("=" * 60)
    print()
    
    # Check Python version
    print("1. Checking Python version...")
    python_ok = check_python_version()
    print()
    
    # Check dependencies
    print("2. Checking dependencies...")
    deps_ok = check_dependencies()
    print()
    
    # Check simulation imports
    print("3. Checking simulation modules...")
    sim_ok = check_simulation_imports()
    print()
    
    # Check modern GUI
    print("4. Checking modern GUI...")
    gui_ok = check_modern_gui()
    print()
    
    # Summary
    print("=" * 60)
    print("VERIFICATION SUMMARY")
    print("=" * 60)
    
    if python_ok and deps_ok and sim_ok and gui_ok:
        print("[SUCCESS] All checks passed!")
        print()
        print("You can now run the modern GUI with:")
        print("  python run_modern_gui.py")
        print()
        print("Or try the demo scenarios with:")
        print("  python demo_modern_gui.py")
        return True
    else:
        print("[ERROR] Some checks failed!")
        print()
        print("Please fix the issues above and run this script again.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
