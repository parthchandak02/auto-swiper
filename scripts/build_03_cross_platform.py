#!/usr/bin/env python3
"""
Cross-Platform Auto-Swiper Build Script
Creates standalone executables for Windows, macOS, and Linux
"""

import os
import sys
import platform
import subprocess
from pathlib import Path

def get_platform_config():
    """Get platform-specific build configuration"""
    system = platform.system().lower()
    
    configs = {
        'windows': {
            'separator': ';',
            'executable_extension': '.exe',
            'icon_option': '--icon=logo.ico',  # Windows uses .ico
            'extra_options': ['--hidden-import=win32gui', '--hidden-import=win32con']
        },
        'darwin': {  # macOS
            'separator': ':',
            'executable_extension': '',
            'icon_option': '--icon=logo.icns',  # macOS uses .icns
            'extra_options': ['--osx-bundle-identifier=com.autoswiper.app']
        },
        'linux': {
            'separator': ':',
            'executable_extension': '',
            'icon_option': '--icon=logo.png',
            'extra_options': []
        }
    }
    
    return configs.get(system, configs['linux'])

def create_platform_executable():
    """Create executable for current platform"""
    config = get_platform_config()
    system = platform.system()
    
    print(f"🚀 Building Auto-Swiper for {system}...")
    
    # Base command
    cmd = [
        'pyinstaller',
        '--onefile',
        '--clean',
        f'--add-data=Images{config["separator"]}Images',
        f'--add-data=jokes.txt{config["separator"]}.',
        '--hidden-import=rich',
        '--hidden-import=rich.console',
        '--hidden-import=rich.progress',
        '--name=AutoSwiper',
        config['icon_option'],
    ]
    
    # Add platform-specific options
    cmd.extend(config['extra_options'])
    
    # Add console option based on platform
    if system == 'Windows':
        cmd.append('--noconsole')  # Hide console on Windows
    else:
        cmd.append('--console')    # Keep console on Unix-like systems
    
    cmd.append('main.py')
    
    print(f"📦 Command: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        executable_name = f"AutoSwiper{config['executable_extension']}"
        print(f"✅ Build successful for {system}!")
        print(f"📁 Executable: dist/{executable_name}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed for {system}!")
        print(f"Error: {e.stderr}")
        return False

def create_github_actions_workflow():
    """Create GitHub Actions workflow for automated builds"""
    workflow_content = '''name: Build Auto-Swiper Executables

on:
  push:
    tags:
      - 'v*'
  workflow_dispatch:

jobs:
  build:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        include:
          - os: windows-latest
            artifact_name: AutoSwiper.exe
            asset_name: AutoSwiper-Windows.exe
          - os: macos-latest
            artifact_name: AutoSwiper
            asset_name: AutoSwiper-macOS
          - os: ubuntu-latest
            artifact_name: AutoSwiper
            asset_name: AutoSwiper-Linux

    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pyinstaller
    
    - name: Build executable
              run: python scripts/build_03_cross_platform.py
    
    - name: Upload artifact
      uses: actions/upload-artifact@v4
      with:
        name: ${{ matrix.asset_name }}
        path: dist/${{ matrix.artifact_name }}
    
    - name: Release
      uses: softprops/action-gh-release@v1
      if: startsWith(github.ref, 'refs/tags/')
      with:
        files: dist/${{ matrix.artifact_name }}
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
'''
    
    # Create .github/workflows directory
    workflow_dir = Path('.github/workflows')
    workflow_dir.mkdir(parents=True, exist_ok=True)
    
    workflow_file = workflow_dir / 'build.yml'
    with open(workflow_file, 'w') as f:
        f.write(workflow_content)
    
    print(f"📝 Created GitHub Actions workflow: {workflow_file}")

def main():
    print("🌍 Auto-Swiper Cross-Platform Build Tool")
    print("=" * 50)
    
    if len(sys.argv) > 1 and sys.argv[1] == '--github-actions':
        create_github_actions_workflow()
        return
    
    # Check if required files exist
    required_files = ['main.py', 'Images', 'jokes.txt']
    missing_files = [f for f in required_files if not os.path.exists(f)]
    
    if missing_files:
        print(f"❌ Missing required files: {missing_files}")
        return
    
    success = create_platform_executable()
    
    if success:
        system = platform.system()
        print(f"\n🎉 {system} build completed successfully!")
        print("\n📋 Distribution Guide:")
        print(f"• {system} users can run the executable directly")
        print("• No Python installation required")
        print("• All dependencies are bundled")
        
        if system == 'Darwin':  # macOS
            print("\n🍎 macOS Notes:")
            print("• Users may need to right-click → Open for first run")
            print("• Or run: xattr -d com.apple.quarantine AutoSwiper")
        elif system == 'Windows':
            print("\n🪟 Windows Notes:")
            print("• Antivirus may flag the executable (false positive)")
            print("• Consider code signing for production distribution")
        
        print(f"\n💡 To build for other platforms:")
        print("• Use GitHub Actions (run with --github-actions)")
        print("• Or build on each target platform manually")

if __name__ == '__main__':
    main()