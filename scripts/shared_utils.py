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
    
    # Windows-compatible console setup with proper UTF-8 encoding
    if platform.system() == "Windows":
        # Force UTF-8 encoding on Windows to handle Unicode characters
        import sys
        if hasattr(sys.stdout, 'reconfigure'):
            try:
                sys.stdout.reconfigure(encoding='utf-8')
                sys.stderr.reconfigure(encoding='utf-8')
            except:
                pass
        console = Console(
            force_terminal=True, 
            legacy_windows=False, 
            width=120,
            file=sys.stdout
        )
    else:
        console = Console()
except ImportError:
    HAS_RICH = False
    console = None


def _safe_encode_message(message: str) -> str:
    """Safely encode message for Windows compatibility"""
    if platform.system() == "Windows":
        # Replace problematic Unicode characters with Windows-safe alternatives
        replacements = {
            '🚀': '[ROCKET]',
            '🎯': '[TARGET]', 
            '📦': '[PACKAGE]',
            '✅': '[OK]',
            '❌': '[ERROR]',
            '⚠️': '[WARN]',
            'ℹ️': '[INFO]',
            '🧹': '[CLEAN]',
            '🌍': '[GLOBE]',
            '🔧': '[TOOL]',
            '🍎': '[APPLE]',
            '🪟': '[WINDOWS]',
            '💡': '[IDEA]',
            '📋': '[CLIPBOARD]',
            '📊': '[CHART]',
            '🎉': '[PARTY]',
            '🔍': '[SEARCH]',
            '⚡': '[ZAP]',
            '🖥️': '[COMPUTER]',
            '🐍': '[SNAKE]'
        }
        
        for emoji, replacement in replacements.items():
            message = message.replace(emoji, replacement)
    
    return message


def print_styled(message: str, style: str = "info") -> None:
    """Print with Rich styling if available, otherwise plain text"""
    # Ensure message is Windows-safe
    safe_message = _safe_encode_message(message)
    
    if HAS_RICH and console:
        styles = {
            "info": "blue",
            "success": "green bold",
            "warning": "yellow",
            "error": "red bold",
            "highlight": "magenta bold",
            "progress": "cyan"
        }
        try:
            console.print(f"[{styles.get(style, 'white')}]{safe_message}[/]")
        except UnicodeEncodeError:
            # Fallback to plain print if Rich still fails
            print(f"{safe_message}")
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
        safe_icon = _safe_encode_message(icons.get(style, ''))
        print(f"{safe_icon} {safe_message}")


def show_banner(title: str, subtitle: str = "", style: str = "blue") -> None:
    """Display a beautiful startup banner"""
    # Ensure title and subtitle are Windows-safe
    safe_title = _safe_encode_message(title)
    safe_subtitle = _safe_encode_message(subtitle)
    
    if HAS_RICH and console:
        try:
            banner_text = Text(safe_title, style=f"bold {style}")
            banner = Panel(
                banner_text,
                subtitle=safe_subtitle if safe_subtitle else None,
                box=box.DOUBLE_EDGE,
                style=style
            )
            console.print(banner)
        except UnicodeEncodeError:
            # Fallback to plain text banner
            print(safe_title)
            if safe_subtitle:
                print(safe_subtitle)
            print("=" * len(safe_title))
    else:
        print(safe_title)
        if safe_subtitle:
            print(safe_subtitle)
        print("=" * len(safe_title))


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
            'executable_extension': '.app',
            'icon_option': '--icon=logo.icns',
            'extra_options': [
                '--osx-bundle-identifier=com.autoswiper.app',
                '--windowed'  # Create .app bundle instead of bare executable
                # Note: --target-architecture=universal2 removed temporarily for compatibility
            ]
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
    
    # Ensure all content is Windows-safe
    safe_build_type = _safe_encode_message(build_type)
    safe_additional_info = [_safe_encode_message(info) for info in additional_info]
    
    if HAS_RICH and console:
        try:
            info_text = "\n".join([f"  • {info}" for info in safe_additional_info])
            safe_info_text = _safe_encode_message(info_text)
            content = f"[green]🎉 {safe_build_type} build completed successfully![/green]"
            safe_content = _safe_encode_message(content)
            
            if safe_info_text:
                safe_content += f"\n\n[bold]📋 Information:[/bold]\n{safe_info_text}"
                safe_content = _safe_encode_message(safe_content)
            
            success_panel = Panel(
                safe_content,
                title="Build Complete",
                box=box.ROUNDED,
                style="green"
            )
            console.print(success_panel)
        except UnicodeEncodeError:
            # Fallback to plain text
            print_styled(f"\n{safe_build_type} build completed successfully!", "success")
            for info in safe_additional_info:
                print_styled(f"  • {info}", "info")
    else:
        print_styled(f"\n{safe_build_type} build completed successfully!", "success")
        for info in safe_additional_info:
            print_styled(f"  • {info}", "info")


def create_dependency_table(dependencies: Dict[str, str]) -> None:
    """Create a Rich table showing dependencies"""
    safe_title = _safe_encode_message("📋 Dependencies")
    
    if HAS_RICH and console:
        try:
            table = Table(title=safe_title, box=box.ROUNDED)
            table.add_column("Package", style="cyan")
            table.add_column("Version", style="green")
            
            for name, version in dependencies.items():
                safe_name = _safe_encode_message(name)
                safe_version = _safe_encode_message(version)
                table.add_row(safe_name, safe_version)
            
            console.print(table)
        except UnicodeEncodeError:
            # Fallback to plain text
            print_styled(safe_title, "info")
            for name, version in dependencies.items():
                print_styled(f"  {name}: {version}", "info")
    else:
        print_styled(safe_title, "info")
        for name, version in dependencies.items():
            print_styled(f"  {name}: {version}", "info")


def check_python_version() -> bool:
    """Check Python version and show recommendations"""
    import sys
    
    python_version = sys.version_info
    if python_version >= (3, 11):
        print_styled(f"Python {python_version.major}.{python_version.minor} - Excellent! Using latest optimizations", "success")
        return True
    elif python_version >= (3, 9):
        print_styled(f"Python {python_version.major}.{python_version.minor} - Good compatibility", "success")
        return True
    elif python_version >= (3, 8):
        print_styled(f"Python {python_version.major}.{python_version.minor} - Consider upgrading to 3.11+ for better performance", "warning")
        return True
    else:
        print_styled(f"Python 3.8+ required, found {python_version.major}.{python_version.minor}", "error")
        return False


def check_tool_availability(tool: str) -> bool:
    """Check if a tool is available in PATH"""
    try:
        subprocess.run([tool, "--version"], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False