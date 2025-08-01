#!/usr/bin/env python3
"""
Shared utilities for Auto-Swiper build scripts
Common functions to eliminate code duplication
"""

import os
import platform
import subprocess
from pathlib import Path
from typing import Dict, Any, Optional, List

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


def show_banner(title: str, subtitle: str = "", style: str = "blue") -> None:
    """Display a beautiful startup banner"""
    if HAS_RICH and console:
        banner_text = Text(title, style=f"bold {style}")
        banner = Panel(
            banner_text,
            subtitle=subtitle if subtitle else None,
            box=box.DOUBLE_EDGE,
            style=style
        )
        console.print(banner)
    else:
        print(title)
        if subtitle:
            print(subtitle)
        print("=" * len(title))


def run_with_progress(cmd: List[str], description: str = "Running command...") -> bool:
    """Run a command with progress indicator"""
    try:
        if HAS_RICH and console:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TimeElapsedColumn(),
                console=console,
            ) as progress:
                progress.add_task(description, total=None)
                subprocess.run(cmd, check=True, capture_output=True, text=True)
        else:
            subprocess.run(cmd, check=True, capture_output=True, text=True)
        return True
    except subprocess.CalledProcessError as e:
        print_styled(f"Command failed: {' '.join(cmd)}", "error")
        if e.stderr:
            print_styled(f"Error: {e.stderr}", "error")
        return False


def check_file_exists(files: List[str]) -> List[str]:
    """Check if required files exist, return list of missing files"""
    return [f for f in files if not os.path.exists(f)]


def get_executable_size(exe_path: str) -> Optional[float]:
    """Get executable size in MB"""
    path = Path(exe_path)
    if path.exists():
        return path.stat().st_size / (1024 * 1024)
    return None


def get_platform_config() -> Dict[str, Any]:
    """Get platform-specific build configuration"""
    system = platform.system().lower()
    
    configs = {
        'windows': {
            'separator': ';',
            'executable_extension': '.exe',
            'icon_option': '--icon=logo.ico',
            'extra_options': ['--hidden-import=win32gui', '--hidden-import=win32con']
        },
        'darwin': {  # macOS
            'separator': ':',
            'executable_extension': '',
            'icon_option': '--icon=logo.icns',
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


def get_common_pyinstaller_args() -> List[str]:
    """Get common PyInstaller arguments used across builds"""
    config = get_platform_config()
    
    return [
        '--onefile',
        '--clean',
        '--noconfirm',
        f'--add-data=Images{config["separator"]}Images',
        f'--add-data=jokes.txt{config["separator"]}.',
        '--name=AutoSwiper',
        
        # Common hidden imports
        '--hidden-import=pyautogui',
        '--hidden-import=cv2',
        '--hidden-import=PIL',
        '--hidden-import=numpy',
        '--hidden-import=rich',
        '--hidden-import=rich.console',
        '--hidden-import=rich.progress',
        '--hidden-import=rich.table',
        '--hidden-import=rich.panel',
        '--hidden-import=rich.text',
        '--hidden-import=rich.box',
    ]


def get_pyinstaller_analysis_config() -> str:
    """Get common PyInstaller Analysis configuration"""
    return '''
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
        'rich.panel',
        'rich.text',
        'rich.box'
    ],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)
'''


def get_pyinstaller_exe_config(console_mode: bool = False, enable_upx: bool = True) -> str:
    """Get common PyInstaller EXE configuration"""
    return f'''
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
    strip=True,
    upx={str(enable_upx).lower()},
    upx_exclude=[],
    runtime_tmpdir=None,
    console={str(console_mode).lower()},
)
'''


def clean_build_directories(directories: List[str] = None) -> None:
    """Clean build directories"""
    if directories is None:
        directories = ['build', 'dist', '__pycache__']
    
    print_styled("🧹 Cleaning build directories...", "info")
    
    for dir_name in directories:
        if os.path.exists(dir_name):
            print_styled(f"  Removing: {dir_name}", "info")
            import shutil
            shutil.rmtree(dir_name)


def show_success_summary(build_type: str, additional_info: List[str] = None) -> None:
    """Show build success summary with Rich panel"""
    if additional_info is None:
        additional_info = []
    
    if HAS_RICH and console:
        info_text = "\n".join([f"  • {info}" for info in additional_info])
        content = f"[green]🎉 {build_type} build completed successfully![/green]"
        if info_text:
            content += f"\n\n[bold]📋 Information:[/bold]\n{info_text}"
        
        success_panel = Panel(
            content,
            title="Build Complete",
            box=box.ROUNDED,
            style="green"
        )
        console.print(success_panel)
    else:
        print_styled(f"\n🎉 {build_type} build completed successfully!", "success")
        for info in additional_info:
            print_styled(f"  • {info}", "info")


def create_dependency_table(dependencies: Dict[str, str]) -> None:
    """Create a Rich table showing dependencies"""
    if HAS_RICH and console:
        table = Table(title="📋 Dependencies", box=box.ROUNDED)
        table.add_column("Package", style="cyan")
        table.add_column("Version", style="green")
        
        for name, version in dependencies.items():
            table.add_row(name, version)
        
        console.print(table)
    else:
        print_styled("📋 Dependencies:", "info")
        for name, version in dependencies.items():
            print_styled(f"  {name}: {version}", "info")


def check_python_version() -> bool:
    """Check Python version and show recommendations"""
    import sys
    
    python_version = sys.version_info
    if python_version >= (3, 11):
        print_styled(f"✅ Python {python_version.major}.{python_version.minor} - Excellent! Using latest optimizations", "success")
        return True
    elif python_version >= (3, 9):
        print_styled(f"✅ Python {python_version.major}.{python_version.minor} - Good compatibility", "success")
        return True
    elif python_version >= (3, 8):
        print_styled(f"⚠️ Python {python_version.major}.{python_version.minor} - Consider upgrading to 3.11+ for better performance", "warning")
        return True
    else:
        print_styled(f"❌ Python 3.8+ required, found {python_version.major}.{python_version.minor}", "error")
        return False


def check_tool_availability(tool: str) -> bool:
    """Check if a tool is available in PATH"""
    try:
        subprocess.run([tool, "--version"], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False