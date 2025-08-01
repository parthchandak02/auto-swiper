#!/usr/bin/env python3
"""
Auto-Swiper Build Optimization Script
Reduces executable size and optimizes packaging
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

def create_optimized_spec():
    """Create an optimized PyInstaller spec file"""
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

# Optimized Auto-Swiper build configuration

block_cipher = None

# Modules to exclude (reduce size)
excludes = [
    'matplotlib',
    'scipy',
    'pandas',
    'jupyter',
    'IPython',
    'notebook',
    'tkinter',
    'PyQt5',
    'PyQt6',
    'PySide2',
    'PySide6',
    'wx',
    'doctest',
    'unittest',
    'test',
    'tests',
    'distutils',
    'setuptools',
    'pip',
    'wheel',
]

a = Analysis(
    ['main.py'],
    pathex=['.'],
    binaries=[],
    datas=[
        ('Images', 'Images'),
        ('jokes.txt', '.'),
    ],
    hiddenimports=[
        'pyautogui',
        'cv2',
        'PIL',
        'numpy',
        'rich',
        'rich.console',
        'rich.progress',
        'rich.table',
        'rich.panel'
    ],
    hookspath=[],
    runtime_hooks=[],
    excludes=excludes,
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# Remove duplicate and unnecessary files
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='AutoSwiper',
    debug=False,
    bootloader_ignore_signals=False,
    strip=True,           # Strip debug symbols
    upx=True,            # Use UPX compression
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,        # No console window
    icon='logo.png'
)
'''
    
    with open('AutoSwiper_optimized.spec', 'w') as f:
        f.write(spec_content)
    
    print("📝 Created optimized spec file: AutoSwiper_optimized.spec")

def build_optimized():
    """Build optimized executable"""
    print("🔧 Building optimized Auto-Swiper executable...")
    
    # Clean previous builds
    build_dirs = ['build', 'dist']
    for dir_name in build_dirs:
        if os.path.exists(dir_name):
            print(f"🧹 Cleaning {dir_name}...")
            shutil.rmtree(dir_name)
    
    cmd = ['pyinstaller', 'AutoSwiper_optimized.spec']
    
    print(f"📦 Running: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✅ Optimized build successful!")
        
        # Check file size
        exe_path = Path('dist/AutoSwiper')
        if exe_path.exists():
            size_mb = exe_path.stat().st_size / (1024 * 1024)
            print(f"📊 Executable size: {size_mb:.1f} MB")
        
        return True
    except subprocess.CalledProcessError as e:
        print("❌ Optimized build failed!")
        print(f"Error: {e.stderr}")
        return False

def analyze_dependencies():
    """Analyze which dependencies are taking up space"""
    print("🔍 Analyzing dependencies...")
    
    try:
        # Get dependency tree
        result = subprocess.run(['pip', 'show', 'pyautogui', 'opencv-python', 'pillow'], 
                              capture_output=True, text=True)
        print("📋 Main dependencies:")
        print(result.stdout)
        
        # Show largest packages
        result = subprocess.run(['pip', 'list'], capture_output=True, text=True)
        print("\n📦 All installed packages:")
        for line in result.stdout.split('\n')[2:10]:  # Show first 10 packages
            if line.strip():
                print(f"  {line}")
                
    except Exception as e:
        print(f"❌ Error analyzing dependencies: {e}")

def create_minimal_requirements():
    """Create minimal requirements.txt for smaller builds"""
    minimal_deps = [
        "pyautogui>=0.9.54",
        "opencv-python>=4.8.0",
        "pillow>=10.0.0",
    ]
    
    with open('requirements_minimal.txt', 'w') as f:
        f.write('\n'.join(minimal_deps) + '\n')
    
    print("📝 Created minimal requirements: requirements_minimal.txt")
    print("💡 Use this for smaller builds: pip install -r requirements_minimal.txt")

def main():
    print("🎯 Auto-Swiper Build Optimizer")
    print("=" * 50)
    
    if len(sys.argv) > 1:
        action = sys.argv[1]
        
        if action == '--analyze':
            analyze_dependencies()
        elif action == '--minimal':
            create_minimal_requirements()
        elif action == '--spec':
            create_optimized_spec()
        elif action == '--build':
            create_optimized_spec()
            build_optimized()
        else:
            print(f"❌ Unknown action: {action}")
            print("Available actions: --analyze, --minimal, --spec, --build")
    else:
        print("🔧 Available optimization options:")
        print("  --analyze    : Analyze current dependencies")
        print("  --minimal    : Create minimal requirements.txt")
        print("  --spec       : Create optimized PyInstaller spec")
        print("  --build      : Build optimized executable")
        print("\nExample: python scripts/build_02_optimized.py --build")

if __name__ == '__main__':
    main()