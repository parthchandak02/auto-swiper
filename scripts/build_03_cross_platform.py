#!/usr/bin/env python3
"""
Cross-Platform Auto-Swiper Build Script
Creates standalone executables for Windows, macOS, and Linux
"""

import sys
import platform
import subprocess
# Handle imports for both direct execution and module import
try:
    from .shared_utils import (
        print_styled, show_banner, check_file_exists,
        get_platform_config, show_success_summary, HAS_RICH, console
    )
except ImportError:
    from shared_utils import (
        print_styled, show_banner, check_file_exists,
        get_platform_config, show_success_summary, HAS_RICH, console
    )

try:
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
except ImportError:
    # Define dummy classes for when Rich is not available
    class Progress:
        def __init__(self, *args, **kwargs): pass
        def __enter__(self): return self
        def __exit__(self, *args): pass
        def add_task(self, *args, **kwargs): pass
    
    class SpinnerColumn: pass
    class TextColumn: pass
    class BarColumn: pass
    class TimeElapsedColumn: pass







def create_platform_executable():
    """Create executable for current platform"""
    config = get_platform_config()
    system = platform.system()
    
    print_styled(f"🚀 Building Auto-Swiper for {system}...", "highlight")
    
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
    elif system == 'Darwin':
        # macOS .app bundles are windowed by default (specified in extra_options)
        pass  # --windowed already included in extra_options
    else:
        cmd.append('--console')    # Keep console on Linux
    
    cmd.append('main.py')
    
    print_styled(f"📦 Command: {' '.join(cmd)}", "progress")
    
    try:
        if HAS_RICH and console:
            # Show progress with Rich
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TimeElapsedColumn(),
                console=console,
            ) as progress:
                progress.add_task(f"Building for {system}...", total=None)
                subprocess.run(cmd, check=True, capture_output=True, text=True)
        else:
            # Fallback without Rich
            subprocess.run(cmd, check=True, capture_output=True, text=True)
            
        executable_name = f"AutoSwiper{config['executable_extension']}"
        print_styled(f"✅ Build successful for {system}!", "success")
        print_styled(f"📁 Executable: dist/{executable_name}", "info")
        return True
    except subprocess.CalledProcessError as e:
        print_styled(f"❌ Build failed for {system}!", "error")
        print_styled(f"Error: {e.stderr}", "error")
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
                    curl -LsSf https://astral.sh/uv/install.sh | sh
            export PATH="$HOME/.cargo/bin:$PATH"
            uv pip install --system -r requirements.txt
            uv pip install --system pyinstaller
    
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
    
    print_styled(f"📝 Created GitHub Actions workflow: {workflow_file}", "success")

def main():
    system = platform.system()
    
    # Windows-safe text without emojis
    if system == "Windows":
        title_text = "Auto-Swiper Cross-Platform Build Tool"
    else:
        title_text = "🌍 Auto-Swiper Cross-Platform Build Tool"
    
    show_banner(
        title_text,
        f"Building for {system} with universal compatibility",
        "cyan"
    )
    
    if len(sys.argv) > 1 and sys.argv[1] == '--github-actions':
        create_github_actions_workflow()
        return
    
    # Check if required files exist
    required_files = ['main.py', 'Images', 'jokes.txt']
    missing_files = check_file_exists(required_files)
    
    if missing_files:
        print_styled(f"❌ Missing required files: {missing_files}", "error")
        return
    
    success = create_platform_executable()
    
    if success:
        system = platform.system()
        
        show_success_summary(
            f"{system}",
            [
                f"{system} users can run the executable directly",
                "No Python installation required",
                "All dependencies are bundled"
            ]
        )
        
        if system == 'Darwin':  # macOS
            print_styled("\n🍎 macOS Notes:", "warning")
            print_styled("• Users may need to right-click → Open for first run", "info")
            print_styled("• Or run: xattr -d com.apple.quarantine AutoSwiper", "info")
        elif system == 'Windows':
            print_styled("\n🪟 Windows Notes:", "warning")
            print_styled("• Antivirus may flag the executable (false positive)", "info")
            print_styled("• Consider code signing for production distribution", "info")
        
        print_styled("\n💡 To build for other platforms:", "info")
        print_styled("• Use GitHub Actions (run with --github-actions)", "info")
        print_styled("• Or build on each target platform manually", "info")

if __name__ == '__main__':
    main()