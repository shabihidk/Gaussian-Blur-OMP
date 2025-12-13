#!/usr/bin/env python3
"""Quick dependency check for the GUI app."""

import sys

def check():
    required = {
        'PyQt5': 'PyQt5',
        'PIL': 'Pillow',
        'cv2': 'opencv-python',
        'numpy': 'numpy',
        'matplotlib': 'matplotlib',
        'pandas': 'pandas',
        'psutil': 'psutil',
    }
    
    missing = []
    print("Checking dependencies...\n")
    
    for module, package in required.items():
        try:
            __import__(module)
            print(f"✓ {package}")
        except ImportError:
            print(f"✗ {package} - MISSING")
            missing.append(package)
    
    if missing:
        print(f"\n❌ Install missing packages:")
        print(f"   pip install {' '.join(missing)}")
        return False
    
    print("\n✅ All set! Run: python main.py")
    return True

if __name__ == '__main__':
    sys.exit(0 if check() else 1)
