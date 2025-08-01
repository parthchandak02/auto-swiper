#!/usr/bin/env python3
"""
Auto-Swiper Quick Build Script (2025 Edition)
Fast development builds for local testing with modern optimizations
"""

import os
import sys
import shutil
import subprocess
import argparse
import time
from pathlib import Path
from typing import List, Optional

# Rich imports for beautiful terminal output
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
    from rich.table import Table
    from rich.text import Text
    from rich import box
    HAS_RICH = True
    console = Console()
except ImportError:
    HAS_RICH = False
    console = None

# Modern Python features and optimizations
if sys.version_info >= (3, 11):
    # Use faster startup in Python 3.11+
    import tomllib  # Built-in TOML support in 3.11+
    PYTHON_OPTIMIZED = True
else:
    PYTHON_OPTIMIZED = False

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
        # Fallback icons for non-Rich environments
        icons = {
            "info": "🔧",
            "success": "✅", 
            "warning": "⚠️",
            "error": "❌",
            "highlight": "🎯",
            "progress": "📦"
        }
        print(f"{icons.get(style, '')} {message}")

def show_banner():
    """Display a beautiful startup banner"""
    if HAS_RICH and console:
        banner = Panel(
            Text("🎯 Auto-Swiper Quick Build Tool (2025 Edition)", style="bold blue"),
            subtitle="Fast development builds with modern optimizations",
            box=box.DOUBLE_EDGE,
            style="blue"
        )
        console.print(banner)
    else:
        print("🎯 Auto-Swiper Quick Build Tool (2025 Edition)")
        print("=" * 55)

def create_build(console_mode: bool = False, use_uv: bool = False) -> bool:
    """Build the auto-swiper executable with modern optimizations"""
    start_time = time.time()
    
    print_styled("🚀 Building Auto-Swiper standalone executable (2025 Edition)...", "highlight")
    
    # Fast dependency check using uv if available
    if use_uv:
        print_styled("⚡ Using uv for faster dependency resolution...", "info")
        try:
            subprocess.run(['uv', 'pip', 'install', 'pyinstaller'], check=True, capture_output=True)
        except (FileNotFoundError, subprocess.CalledProcessError):
            print_styled("📦 Falling back to pip...", "warning")
            use_uv = False
    
    # Clean previous builds
    build_dirs = ['build', 'dist', '__pycache__']
    for dir_name in build_dirs:
        if os.path.exists(dir_name):
            print_styled(f"🧹 Cleaning {dir_name}...", "info")
            shutil.rmtree(dir_name)
    
    # Determine platform-specific settings
    import platform
    system = platform.system()
    
    # Enhanced PyInstaller command with 2025 optimizations
    cmd = [
        'pyinstaller',
        '--onefile',                           # Create single executable
        '--clean',                             # Clean PyInstaller cache
        '--noconfirm',                         # Overwrite without confirmation
        '--add-data', f'Images{os.pathsep}Images',  # Cross-platform path separator
        '--add-data', f'jokes.txt{os.pathsep}.',    # Include jokes.txt in root
        '--name', 'AutoSwiper',                # Name of executable
        '--distpath', 'dist',                  # Output directory
        
        # Hidden imports for Rich library (2025 addition)
        '--hidden-import', 'rich',
        '--hidden-import', 'rich.console',
        '--hidden-import', 'rich.progress',
        '--hidden-import', 'rich.table',
        '--hidden-import', 'rich.panel',
        '--hidden-import', 'rich.text',
        '--hidden-import', 'rich.live',
        '--hidden-import', 'rich.box',
        
        # Standard hidden imports
        '--hidden-import', 'pyautogui',
        '--hidden-import', 'cv2',
        '--hidden-import', 'PIL',
        '--hidden-import', 'numpy',
        
        # Performance optimizations for Python 3.11+
        '--strip',                             # Remove debug symbols
        
        'main.py'                              # Entry point
    ]
    
    # Console mode handling
    if console_mode:
        cmd.append('--console')
        print_styled("🖥️ Building with console window (debug mode)", "info")
    else:
        cmd.append('--noconsole')
    
    # Add icon if available
    icon_files = ['logo.png', 'logo.ico', 'icon.png', 'icon.ico']
    for icon_file in icon_files:
        if os.path.exists(icon_file):
            cmd.extend(['--icon', icon_file])
            print_styled(f"🎨 Using icon: {icon_file}", "info")
            break
    
    # Platform-specific optimizations
    if system == "Windows":
        cmd.extend([
            '--version-file', 'version.txt'  # If version file exists
        ]) if os.path.exists('version.txt') else None
    elif system == "Darwin":  # macOS
        cmd.extend([
            '--osx-bundle-identifier', 'com.autoswiper.app'
        ])
    
    # Python 3.11+ specific optimizations
    if PYTHON_OPTIMIZED:
        cmd.extend([
            '--optimize', '2',                 # Maximum optimization
            '--exclude-module', 'test',        # Exclude test modules
            '--exclude-module', 'unittest',    # Exclude unittest
        ])
        print_styled("⚡ Using Python 3.11+ optimizations", "info")
    
    print_styled("📦 Running PyInstaller with modern optimizations...", "progress")
    print_styled(f"🔧 Command: {' '.join(cmd)}", "info")
    
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
                task = progress.add_task("Building executable...", total=None)
                result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        else:
            # Fallback without Rich
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        
        build_time = time.time() - start_time
        print_styled(f"✅ Build successful in {build_time:.1f} seconds!", "success")
        
        # Check executable size and provide info
        exe_path = Path('dist/AutoSwiper')
        if system == "Windows":
            exe_path = Path('dist/AutoSwiper.exe')
        
        if exe_path.exists():
            size_mb = exe_path.stat().st_size / (1024 * 1024)
            print_styled(f"📊 Executable size: {size_mb:.1f} MB", "info")
            print_styled(f"📁 Executable created: {exe_path}", "success")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print_styled("❌ Build failed!", "error")
        print_styled(f"Error: {e}", "error")
        if e.stdout:
            print_styled(f"Output: {e.stdout}", "error")
        if e.stderr:
            print_styled(f"Error output: {e.stderr}", "error")
        return False

def create_spec_file():
    """Create a custom .spec file for more control"""
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

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
        'opencv-python',
        'pillow',
        'numpy',
        'rich',
        'rich.console',
        'rich.progress',
        'rich.table',
        'rich.panel',
        'rich.text'
    ],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

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
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Set to True for debugging
)
'''
    
    with open('AutoSwiper.spec', 'w') as f:
        f.write(spec_content)
    
    print("📝 Created AutoSwiper.spec file")
    print("💡 You can now run: pyinstaller AutoSwiper.spec")

def main():
    """Main function with modern argument parsing"""
    parser = argparse.ArgumentParser(
        description="Auto-Swiper Quick Build Tool (2025 Edition)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/build_01_quick.py                    # Standard build
python scripts/build_01_quick.py --console          # Build with console window
python scripts/build_01_quick.py --spec             # Generate spec file only
python scripts/build_01_quick.py --use-uv           # Use uv for faster builds
        """
    )
    
    parser.add_argument('--spec', action='store_true', 
                       help='Create custom spec file only')
    parser.add_argument('--console', action='store_true',
                       help='Show console window (useful for debugging)')
    parser.add_argument('--use-uv', action='store_true',
                       help='Use uv for faster dependency management')
    parser.add_argument('--no-console', action='store_true',
                       help='Hide console window (default)')
    
    args = parser.parse_args()
    
    show_banner()
    
    if args.spec:
        create_spec_file()
        return True
    
    # Check if required files exist
    required_files = ['main.py', 'Images', 'jokes.txt']
    missing_files = [f for f in required_files if not os.path.exists(f)]
    
    if missing_files:
        print_styled(f"❌ Missing required files: {missing_files}", "error")
        return False
    
    # Check Python version and give recommendations
    python_version = sys.version_info
    if python_version >= (3, 11):
        print_styled(f"✅ Python {python_version.major}.{python_version.minor} - Excellent! Using latest optimizations", "success")
    elif python_version >= (3, 9):
        print_styled(f"✅ Python {python_version.major}.{python_version.minor} - Good compatibility", "success")
    else:
        print_styled(f"⚠️ Python {python_version.major}.{python_version.minor} - Consider upgrading to 3.11+ for better performance", "warning")
    
    # Determine console mode
    console_mode = args.console or not args.no_console
    if args.no_console:
        console_mode = False
    
    # Check for uv availability
    use_uv = args.use_uv
    if use_uv:
        try:
            subprocess.run(['uv', '--version'], capture_output=True, check=True)
            print_styled("⚡ uv detected - will use for faster dependency management", "success")
        except (FileNotFoundError, subprocess.CalledProcessError):
            print_styled("📦 uv not found - falling back to pip", "warning")
            use_uv = False
    
    success = create_build(console_mode=console_mode, use_uv=use_uv)
    
    if success:
        print("\n🎉 Quick build completed successfully!")
        print("\n📋 Next steps:")
        print("  • Test the executable immediately")
        print("  • For production, run: python scripts/build_manager.py optimized")
        print("  • For multiple platforms: python scripts/build_manager.py cross")
        
        # Show performance tips
        print("\n💡 Performance tips:")
        if not PYTHON_OPTIMIZED:
            print("  • Upgrade to Python 3.11+ for 10-15% faster execution")
        if not use_uv:
            print("  • Install uv for faster dependency management: pip install uv")
        
        print(f"\n⚠️ Platform-specific build:")
        print(f"   This executable works on {sys.platform} only")
        
    else:
        print("\n❌ Build failed!")
        print("\n🔧 Troubleshooting:")
        print("  • Check all dependencies are installed: pip install -r requirements.txt")
        print("  • Try with --console flag to see runtime errors")
        print("  • Generate spec file: python scripts/build_01_quick.py --spec")
        
    return success

if __name__ == '__main__':
    sys.exit(0 if main() else 1)