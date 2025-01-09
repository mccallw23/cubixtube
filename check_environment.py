"""
Environment checker for CubixTube visualization.
Verifies Python version and required package versions.
"""
import platform
import sys

def check_environment():
    """Check and print environment details."""
    print("Environment Details:")
    print("-" * 20)
    print(f"Python Platform: {platform.platform()}")
    print(f"Architecture: {platform.machine()}")
    print(f"Python Version: {platform.python_version()}")
    
    # Check required packages
    try:
        import numpy
        print(f"NumPy Version: {numpy.__version__}")
    except ImportError:
        print("NumPy not installed")
    
    try:
        import matplotlib
        print(f"Matplotlib Version: {matplotlib.__version__}")
    except ImportError:
        print("Matplotlib not installed")

if __name__ == "__main__":
    check_environment()
