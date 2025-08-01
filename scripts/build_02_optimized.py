#!/usr/bin/env python3
"""
Auto-Swiper Build Optimization Script
Reduces executable size and optimizes packaging
"""

import sys
import subprocess
# Handle imports for both direct execution and module import
try:
    from .shared_utils import (
        print_styled, show_banner, get_executable_size,
        get_pyinstaller_analysis_config, get_pyinstaller_exe_config,
        clean_build_directories, HAS_RICH, console
    )
except ImportError:
    from shared_utils import (
        print_styled, show_banner, get_executable_size,
        get_pyinstaller_analysis_config, get_pyinstaller_exe_config,
        clean_build_directories, HAS_RICH, console
    )

try:
    from rich.panel import Panel
    from rich.table import Table
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
    from rich import box
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



def create_optimized_spec():
    """Create an optimized PyInstaller spec file"""
    # Additional excludes for size optimization
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
    
    spec_content = f'''# -*- mode: python ; coding: utf-8 -*-

# Optimized Auto-Swiper build configuration

block_cipher = None

# Modules to exclude (reduce size)
excludes = {excludes}

{get_pyinstaller_analysis_config()}

# Override excludes for optimization
a.excludes = excludes

# Remove duplicate and unnecessary files
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

{get_pyinstaller_exe_config(console_mode=False, enable_upx=True)}
'''
    
    with open('AutoSwiper_optimized.spec', 'w') as f:
        f.write(spec_content)
    
    print_styled("📝 Created optimized spec file: AutoSwiper_optimized.spec", "success")

def build_optimized():
    """Build optimized executable"""
    print_styled("🔧 Building optimized Auto-Swiper executable...", "highlight")
    
    # Clean previous builds
    clean_build_directories(['build', 'dist'])
    
    cmd = ['pyinstaller', 'AutoSwiper_optimized.spec']
    
    print_styled(f"📦 Running: {' '.join(cmd)}", "progress")
    
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
                progress.add_task("Building optimized executable...", total=None)
                subprocess.run(cmd, check=True, capture_output=True, text=True)
        else:
            # Fallback without Rich
            subprocess.run(cmd, check=True, capture_output=True, text=True)
            
        print_styled("✅ Optimized build successful!", "success")
        
        # Check file size
        size_mb = get_executable_size('dist/AutoSwiper')
        if size_mb:
            print_styled(f"📊 Executable size: {size_mb:.1f} MB", "info")
        
        return True
    except subprocess.CalledProcessError as e:
        print_styled("❌ Optimized build failed!", "error")
        print_styled(f"Error: {e.stderr}", "error")
        return False

def analyze_dependencies():
    """Analyze which dependencies are taking up space"""
    print_styled("🔍 Analyzing dependencies...", "highlight")
    
    try:
        # Get dependency tree
        result = subprocess.run(['pip', 'show', 'pyautogui', 'opencv-python', 'pillow'], 
                              capture_output=True, text=True)
        
        if HAS_RICH and console:
            deps_table = Table(title="📋 Main Dependencies", box=box.ROUNDED)
            deps_table.add_column("Package", style="cyan")
            deps_table.add_column("Version", style="green")
            
            for line in result.stdout.split('\n'):
                if line.startswith('Name:'):
                    name = line.split(': ')[1]
                elif line.startswith('Version:'):
                    version = line.split(': ')[1]
                    deps_table.add_row(name, version)
            
            console.print(deps_table)
        else:
            print_styled("📋 Main dependencies:", "info")
            print_styled(result.stdout, "info")
        
        # Show largest packages
        result = subprocess.run(['pip', 'list'], capture_output=True, text=True)
        print_styled("\n📦 All installed packages (first 10):", "info")
        for line in result.stdout.split('\n')[2:10]:  # Show first 10 packages
            if line.strip():
                print_styled(f"  {line}", "info")
                
    except Exception as e:
        print_styled(f"❌ Error analyzing dependencies: {e}", "error")

def create_minimal_requirements():
    """Create minimal requirements.txt for smaller builds"""
    minimal_deps = [
        "pyautogui>=0.9.54",
        "opencv-python>=4.8.0",
        "pillow>=10.0.0",
        "rich>=13.0.0",  # Add rich to minimal requirements
    ]
    
    with open('requirements_minimal.txt', 'w') as f:
        f.write('\n'.join(minimal_deps) + '\n')
    
    print_styled("📝 Created minimal requirements: requirements_minimal.txt", "success")
    print_styled("💡 Use this for smaller builds: uv pip install -r requirements_minimal.txt", "info")

def main():
    show_banner(
        "🚀 Auto-Swiper Optimized Build Tool",
        "Size-optimized production builds with advanced compression",
        "magenta"
    )
    
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
            print_styled(f"❌ Unknown action: {action}", "error")
            print_styled("Available actions: --analyze, --minimal, --spec, --build", "info")
    else:
        if HAS_RICH and console:
            options_panel = Panel(
                "[bold]🔧 Available optimization options:[/bold]\n\n"
                "[cyan]--analyze[/cyan]    : Analyze current dependencies\n"
                "[cyan]--minimal[/cyan]    : Create minimal requirements.txt\n"
                "[cyan]--spec[/cyan]       : Create optimized PyInstaller spec\n"
                "[cyan]--build[/cyan]      : Build optimized executable\n\n"
                "[bold]Example:[/bold] [green]python scripts/build_02_optimized.py --build[/green]",
                title="Build Options",
                box=box.ROUNDED,
                style="blue"
            )
            console.print(options_panel)
        else:
            print_styled("🔧 Available optimization options:", "info")
            print_styled("  --analyze    : Analyze current dependencies", "info")
            print_styled("  --minimal    : Create minimal requirements.txt", "info")
            print_styled("  --spec       : Create optimized PyInstaller spec", "info")
            print_styled("  --build      : Build optimized executable", "info")
            print_styled("\nExample: python scripts/build_02_optimized.py --build", "highlight")

if __name__ == '__main__':
    main()