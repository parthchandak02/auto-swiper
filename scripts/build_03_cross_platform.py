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

# Rich imports for beautiful terminal output
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
    from rich.table import Table
    from rich.text import Text
    from rich import box
    HAS_RICH = True
    
    # Windows-compatible console setup
    if platform.system() == "Windows":
        # Windows-safe console without legacy renderer
        console = Console(force_terminal=True, legacy_windows=False, width=120)
    else:
        console = Console()
except ImportError:
    HAS_RICH = False
    console = None

def print_styled(message: str, style: str = "info") -> None:
    """Print with Rich styling if available, otherwise plain text"""
    if HAS_RICH and console:
        styles = {
            "info": "blue",
            "success": "green bold", 
            "warning": "yellow",
            "error": "red bold",
            "highlight": "magenta bold",
            "progress": "cyan"
        }
        console.print(f"[{styles.get(style, 'white')}]{message}[/]")
    else:
        # Fallback icons for non-Rich environments (Windows-safe)
        if platform.system() == "Windows":
            icons = {
                "info": "[INFO]",
                "success": "[OK]", 
                "warning": "[WARN]",
                "error": "[ERROR]",
                "highlight": "[*]",
                "progress": "[BUILD]"
            }
        else:
            icons = {
                "info": "ℹ️",
                "success": "✅", 
                "warning": "⚠️",
                "error": "❌",
                "highlight": "🎯",
                "progress": "📦"
            }
        print(f"{icons.get(style, '')} {message}")

def show_banner():
    """Display a beautiful startup banner"""
    system = platform.system()
    
    # Windows-safe text without emojis
    if system == "Windows":
        title_text = "Auto-Swiper Cross-Platform Build Tool"
        fallback_text = "Auto-Swiper Cross-Platform Build Tool"
    else:
        title_text = "🌍 Auto-Swiper Cross-Platform Build Tool"
        fallback_text = "🌍 Auto-Swiper Cross-Platform Build Tool"
    
    if HAS_RICH and console:
        banner = Panel(
            Text(title_text, style="bold cyan"),
            subtitle=f"Building for {system} with universal compatibility",
            box=box.DOUBLE_EDGE,
            style="cyan"
        )
        console.print(banner)
    else:
        print(fallback_text)
        print(f"Building for {system}")
        print("=" * 60)

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
    else:
        cmd.append('--console')    # Keep console on Unix-like systems
    
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
                task = progress.add_task(f"Building for {system}...", total=None)
                result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        else:
            # Fallback without Rich
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            
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
    show_banner()
    
    if len(sys.argv) > 1 and sys.argv[1] == '--github-actions':
        create_github_actions_workflow()
        return
    
    # Check if required files exist
    required_files = ['main.py', 'Images', 'jokes.txt']
    missing_files = [f for f in required_files if not os.path.exists(f)]
    
    if missing_files:
        print_styled(f"❌ Missing required files: {missing_files}", "error")
        return
    
    success = create_platform_executable()
    
    if success:
        system = platform.system()
        
        if HAS_RICH and console:
            success_panel = Panel(
                f"[green]🎉 {system} build completed successfully![/green]\n\n"
                "[bold]📋 Distribution Guide:[/bold]\n"
                f"• {system} users can run the executable directly\n"
                "• No Python installation required\n"
                "• All dependencies are bundled",
                title="Build Complete",
                box=box.ROUNDED,
                style="green"
            )
            console.print(success_panel)
        else:
            print_styled(f"\n🎉 {system} build completed successfully!", "success")
            print_styled("\n📋 Distribution Guide:", "info")
            print_styled(f"• {system} users can run the executable directly", "info")
            print_styled("• No Python installation required", "info")
            print_styled("• All dependencies are bundled", "info")
        
        if system == 'Darwin':  # macOS
            print_styled("\n🍎 macOS Notes:", "warning")
            print_styled("• Users may need to right-click → Open for first run", "info")
            print_styled("• Or run: xattr -d com.apple.quarantine AutoSwiper", "info")
        elif system == 'Windows':
            print_styled("\n🪟 Windows Notes:", "warning")
            print_styled("• Antivirus may flag the executable (false positive)", "info")
            print_styled("• Consider code signing for production distribution", "info")
        
        print_styled(f"\n💡 To build for other platforms:", "info")
        print_styled("• Use GitHub Actions (run with --github-actions)", "info")
        print_styled("• Or build on each target platform manually", "info")

if __name__ == '__main__':
    main()