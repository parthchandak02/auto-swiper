#!/usr/bin/env python3
"""
Auto-Swiper Build Manager (2025 Edition)
Modern build orchestrator with support for different build types and targets
"""

import argparse
import os
import sys
import subprocess
import json
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum

# Try to use rich for better output, fallback to standard print
try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich.prompt import Confirm
    console = Console()
    HAS_RICH = True
except ImportError:
    HAS_RICH = False
    console = None

class BuildType(Enum):
    """Available build types"""
    QUICK = "quick"           # Fast local development build
    OPTIMIZED = "optimized"   # Size-optimized production build  
    CROSS_PLATFORM = "cross"  # Multi-platform CI/CD build
    ANALYSIS = "analysis"     # Dependency analysis only

class Platform(Enum):
    """Supported platforms"""
    WINDOWS = "windows"
    MACOS = "macos" 
    LINUX = "linux"
    CURRENT = "current"

@dataclass
class BuildConfig:
    """Build configuration settings"""
    build_type: BuildType
    platform: Platform
    output_dir: str = "dist"
    clean_first: bool = True
    enable_upx: bool = True
    console_mode: bool = False
    include_debug: bool = False
    custom_spec: Optional[str] = None

def print_styled(message: str, style: str = "info") -> None:
    """Print with styling if rich is available, otherwise plain text"""
    if HAS_RICH and console:
        styles = {
            "info": "blue",
            "success": "green", 
            "warning": "yellow",
            "error": "red",
            "highlight": "magenta bold"
        }
        console.print(f"[{styles.get(style, 'white')}]{message}[/]")
    else:
        icons = {
            "info": "ℹ️",
            "success": "✅", 
            "warning": "⚠️",
            "error": "❌",
            "highlight": "🎯"
        }
        print(f"{icons.get(style, '')} {message}")

def check_prerequisites() -> bool:
    """Check if all required tools and files are available"""
    print_styled("🔍 Checking prerequisites...", "info")
    
    # Check Python version (3.11+ recommended for best performance)
    python_version = sys.version_info
    if python_version < (3, 8):
        print_styled(f"❌ Python 3.8+ required, found {python_version.major}.{python_version.minor}", "error")
        return False
    
    if python_version < (3, 11):
        print_styled(f"⚠️ Python 3.11+ recommended for best performance (current: {python_version.major}.{python_version.minor})", "warning")
    
    # Check required files
    required_files = ["main.py", "requirements.txt", "Images", "jokes.txt"]
    missing_files = [f for f in required_files if not os.path.exists(f)]
    
    if missing_files:
        print_styled(f"❌ Missing required files: {missing_files}", "error")
        return False
    
    # Check for PyInstaller
    try:
        subprocess.run(["pyinstaller", "--version"], capture_output=True, check=True)
        print_styled("✅ PyInstaller found", "success")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print_styled("❌ PyInstaller not found. Install with: uv pip install pyinstaller", "error")
        return False
    
    # Check for optional tools
    tools_status = {}
    for tool in ["uv", "ruff", "black"]:
        try:
            subprocess.run([tool, "--version"], capture_output=True, check=True)
            tools_status[tool] = True
        except (subprocess.CalledProcessError, FileNotFoundError):
            tools_status[tool] = False
    
    if tools_status["uv"]:
        print_styled("✅ uv found (faster dependency management)", "success")
    else:
        print_styled("💡 Consider installing uv for faster builds: curl -LsSf https://astral.sh/uv/install.sh | sh", "info")
    
    return True

def run_build_script(script_name: str, args: List[str] = None) -> bool:
    """Run a specific build script with error handling"""
    if args is None:
        args = []
    
    script_path = Path(__file__).parent / script_name
    if not script_path.exists():
        print_styled(f"❌ Build script not found: {script_name}", "error")
        return False
    
    cmd = [sys.executable, str(script_path)] + args
    print_styled(f"🚀 Running: {script_name}", "info")
    
    try:
        if HAS_RICH:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console,
            ) as progress:
                task = progress.add_task(f"Building with {script_name}...", total=None)
                result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        else:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        
        print_styled(f"✅ {script_name} completed successfully", "success")
        if result.stdout:
            print_styled("📄 Build output:", "info")
            print(result.stdout)
        return True
        
    except subprocess.CalledProcessError as e:
        print_styled(f"❌ {script_name} failed", "error")
        if e.stderr:
            print_styled("Error details:", "error")
            print(e.stderr)
        return False

def quick_build(config: BuildConfig) -> bool:
    """Run quick development build"""
    print_styled("🏃 Starting quick build for local development", "highlight")
    args = []
    if not config.console_mode:
        args.append("--no-console")
    return run_build_script("build_01_quick.py", args)

def optimized_build(config: BuildConfig) -> bool:
    """Run size-optimized build"""
    print_styled("🎯 Starting optimized build for production", "highlight") 
    args = ["--build"]  # build_02_optimized.py requires --build to actually build
    return run_build_script("build_02_optimized.py", args)

def cross_platform_build(config: BuildConfig) -> bool:
    """Run cross-platform build setup"""
    print_styled("🌍 Setting up cross-platform build", "highlight")
    return run_build_script("build_03_cross_platform.py")

def analyze_build(config: BuildConfig) -> bool:
    """Run build analysis"""
    print_styled("📊 Analyzing build dependencies and size", "highlight")
    return run_build_script("build_02_optimized.py", ["--analyze-only"])

def show_build_status() -> None:
    """Show current build status and available executables"""
    dist_dir = Path("dist")
    if not dist_dir.exists():
        print_styled("No builds found in dist/ directory", "info")
        return
    
    executables = []
    for file_path in dist_dir.rglob("*"):
        if file_path.is_file() and (file_path.suffix in [".exe", ""] and file_path.stem in ["AutoSwiper", "main"]):
            size_mb = file_path.stat().st_size / (1024 * 1024)
            executables.append((str(file_path), f"{size_mb:.1f} MB"))
    
    if not executables:
        print_styled("No executables found in dist/ directory", "warning")
        return
    
    if HAS_RICH:
        table = Table(title="🎯 Available Executables")
        table.add_column("Executable", style="cyan")
        table.add_column("Size", style="magenta")
        
        for exe_path, size in executables:
            table.add_row(exe_path, size)
        
        console.print(table)
    else:
        print("🎯 Available Executables:")
        for exe_path, size in executables:
            print(f"  {exe_path} ({size})")

def main():
    """Main build manager function"""
    parser = argparse.ArgumentParser(description="Auto-Swiper Build Manager (2025 Edition)")
    parser.add_argument(
        "build_type", 
        nargs="?", 
        choices=[bt.value for bt in BuildType],
        default=BuildType.QUICK.value,
        help="Type of build to perform"
    )
    parser.add_argument("--platform", choices=[p.value for p in Platform], default=Platform.CURRENT.value)
    parser.add_argument("--no-clean", action="store_true", help="Skip cleaning build artifacts")
    parser.add_argument("--console", action="store_true", help="Show console window in executable")
    parser.add_argument("--no-upx", action="store_true", help="Disable UPX compression")
    parser.add_argument("--debug", action="store_true", help="Include debug information")
    parser.add_argument("--status", action="store_true", help="Show build status and exit")
    parser.add_argument("--clean", action="store_true", help="Clean build artifacts and exit")
    
    args = parser.parse_args()
    
    # Show banner
    if HAS_RICH:
        console.print(Panel.fit(
            "[bold blue]Auto-Swiper Build Manager (2025 Edition)[/]\n"
            "[dim]Modern Python executable packaging with PyInstaller[/]",
            border_style="blue"
        ))
    else:
        print("🎯 Auto-Swiper Build Manager (2025 Edition)")
        print("=" * 50)
    
    # Handle utility commands
    if args.clean:
        return run_build_script("maint_cleanup.py")
    
    if args.status:
        show_build_status()
        return True
    
    # Check prerequisites
    if not check_prerequisites():
        return False
    
    # Create build configuration
    config = BuildConfig(
        build_type=BuildType(args.build_type),
        platform=Platform(args.platform),
        clean_first=not args.no_clean,
        enable_upx=not args.no_upx,
        console_mode=args.console,
        include_debug=args.debug
    )
    
    # Clean first if requested
    if config.clean_first:
        print_styled("🧹 Cleaning previous build artifacts...", "info")
        run_build_script("maint_cleanup.py")
    
    # Route to appropriate build function
    build_functions = {
        BuildType.QUICK: quick_build,
        BuildType.OPTIMIZED: optimized_build,
        BuildType.CROSS_PLATFORM: cross_platform_build,
        BuildType.ANALYSIS: analyze_build,
    }
    
    success = build_functions[config.build_type](config)
    
    if success:
        print_styled("🎉 Build completed successfully!", "success")
        show_build_status()
        
        # Show next steps
        print_styled("\n💡 Next Steps:", "info")
        if config.build_type == BuildType.QUICK:
            print("  • Test the executable locally")
            print("  • Run 'python scripts/build_manager.py optimized' for production")
        elif config.build_type == BuildType.OPTIMIZED:
            print("  • Distribute the optimized executable to users")
            print("  • Consider cross-platform builds for multi-OS support")
        elif config.build_type == BuildType.CROSS_PLATFORM:
            print("  • Commit and push to trigger GitHub Actions builds")
            print("  • Check releases page for automated multi-platform builds")
    else:
        print_styled("❌ Build failed. Check error messages above.", "error")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)