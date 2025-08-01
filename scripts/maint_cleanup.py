#!/usr/bin/env python3
"""
Auto-Swiper Cleanup Script
Removes build artifacts and temporary files
"""

import os
import shutil
import glob
from pathlib import Path

def clean_build_artifacts():
    """Remove build and distribution artifacts"""
    artifacts = [
        'build/',
        'dist/',
        '*.spec',
        'AutoSwiper_optimized.spec',
        'requirements_minimal.txt'
    ]
    
    print("🧹 Cleaning build artifacts...")
    
    for pattern in artifacts:
        if pattern.endswith('/'):
            # Directory
            if os.path.exists(pattern):
                print(f"  Removing directory: {pattern}")
                shutil.rmtree(pattern)
        else:
            # File pattern
            for file in glob.glob(pattern):
                print(f"  Removing file: {file}")
                os.remove(file)

def clean_python_cache():
    """Remove Python cache files"""
    print("🐍 Cleaning Python cache files...")
    
    # Find and remove __pycache__ directories
    for root, dirs, files in os.walk('.'):
        if '__pycache__' in dirs:
            cache_dir = os.path.join(root, '__pycache__')
            print(f"  Removing: {cache_dir}")
            shutil.rmtree(cache_dir)
            dirs.remove('__pycache__')
    
    # Remove .pyc files
    for pyc_file in glob.glob('**/*.pyc', recursive=True):
        print(f"  Removing: {pyc_file}")
        os.remove(pyc_file)

def clean_os_files():
    """Remove OS-specific files"""
    print("🖥️  Cleaning OS-specific files...")
    
    # macOS
    for ds_store in glob.glob('**/.DS_Store', recursive=True):
        print(f"  Removing: {ds_store}")
        os.remove(ds_store)
    
    # Windows
    for thumbs in glob.glob('**/Thumbs.db', recursive=True):
        print(f"  Removing: {thumbs}")
        os.remove(thumbs)

def main():
    print("🎯 Auto-Swiper Cleanup Tool")
    print("=" * 40)
    
    if not os.path.exists('main.py'):
        print("❌ Error: Run this script from the project root directory")
        return
    
    clean_build_artifacts()
    clean_python_cache()
    clean_os_files()
    
    print("\n✅ Cleanup complete!")
    print("\n📋 Project is now clean and ready for:")
    print("  • Git commits")
    print("  • Distribution")
    print("  • Fresh builds")

if __name__ == '__main__':
    main()