#!/usr/bin/env python3
"""
Auto-Swiper Cleanup Script
Removes build artifacts and temporary files
"""

import os
import shutil
import glob
# Handle imports for both direct execution and module import
try:
    from .shared_utils import print_styled, show_banner, HAS_RICH, console
except ImportError:
    from shared_utils import print_styled, show_banner, HAS_RICH, console

try:
    from rich.table import Table
    from rich.panel import Panel
    from rich import box
except ImportError:
    pass

def clean_build_artifacts():
    """Remove build and distribution artifacts"""
    artifacts = [
        'build/',
        'dist/',
        '*.spec',
        'AutoSwiper_optimized.spec',
        'requirements_minimal.txt'
    ]
    
    print_styled("🧹 Cleaning build artifacts...", "highlight")
    
    for pattern in artifacts:
        if pattern.endswith('/'):
            # Directory
            if os.path.exists(pattern):
                print_styled(f"  Removing directory: {pattern}", "info")
                shutil.rmtree(pattern)
        else:
            # File pattern
            for file in glob.glob(pattern):
                print_styled(f"  Removing file: {file}", "info")
                os.remove(file)

def clean_python_cache():
    """Remove Python cache files"""
    print_styled("🐍 Cleaning Python cache files...", "highlight")
    
    # Find and remove __pycache__ directories
    for root, dirs, _ in os.walk('.'):
        if '__pycache__' in dirs:
            cache_dir = os.path.join(root, '__pycache__')
            print_styled(f"  Removing: {cache_dir}", "info")
            shutil.rmtree(cache_dir)
            dirs.remove('__pycache__')
    
    # Remove .pyc files
    for pyc_file in glob.glob('**/*.pyc', recursive=True):
        print_styled(f"  Removing: {pyc_file}", "info")
        os.remove(pyc_file)

def clean_os_files():
    """Remove OS-specific files"""
    print_styled("🖥️  Cleaning OS-specific files...", "highlight")
    
    # macOS
    for ds_store in glob.glob('**/.DS_Store', recursive=True):
        print_styled(f"  Removing: {ds_store}", "info")
        os.remove(ds_store)
    
    # Windows
    for thumbs in glob.glob('**/Thumbs.db', recursive=True):
        print_styled(f"  Removing: {thumbs}", "info")
        os.remove(thumbs)

def show_summary(cleaned_items):
    """Display a beautiful cleanup summary"""
    if HAS_RICH and console:
        # Create a summary table
        summary_table = Table(title="🧹 Cleanup Summary", box=box.ROUNDED)
        summary_table.add_column("Category", style="cyan")
        summary_table.add_column("Items Cleaned", style="green")
        
        for category, count in cleaned_items.items():
            summary_table.add_row(category, str(count))
        
        console.print(summary_table)
        
        # Create completion panel
        completion_panel = Panel(
            "[green]✅ Cleanup complete![/green]\n\n"
            "[bold]📋 Project is now clean and ready for:[/bold]\n"
            "  • Git commits\n"
            "  • Distribution\n"
            "  • Fresh builds",
            title="Cleanup Complete",
            box=box.ROUNDED,
            style="green"
        )
        console.print(completion_panel)
    else:
        print_styled("\n✅ Cleanup complete!", "success")
        print_styled("\n📋 Project is now clean and ready for:", "info")
        print_styled("  • Git commits", "info")
        print_styled("  • Distribution", "info")
        print_styled("  • Fresh builds", "info")

def main():
    show_banner(
        "🧹 Auto-Swiper Cleanup Tool",
        "Removing build artifacts and temporary files",
        "blue"
    )
    
    if not os.path.exists('main.py'):
        print_styled("❌ Error: Run this script from the project root directory", "error")
        return
    
    # Track what we cleaned for summary
    cleaned_items = {
        "Build artifacts": 0,
        "Python cache files": 0,
        "OS-specific files": 0
    }
    
    clean_build_artifacts()
    clean_python_cache()
    clean_os_files()
    
    show_summary(cleaned_items)

if __name__ == '__main__':
    main()