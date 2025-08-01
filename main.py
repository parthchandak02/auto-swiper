import pyautogui
import time
from datetime import datetime
import random
import sys
import os

# Rich imports for beautiful terminal output
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich import box

# Initialize Rich console
console = Console()

def get_resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Image paths - properly handled for PyInstaller
roseCheckImg = get_resource_path('Images/0_CHECK_FOR_ROSE.png')
heartImg = get_resource_path('Images/1_HEART.png')
commentImg = get_resource_path('Images/2_ADD_COMMENT.png')
likeImg = get_resource_path('Images/3_SEND_LIKE.png')

# Counters
counter = 0
imgCounter = 0
skipCounter = 0

# Start time
s = datetime.now().strftime("%m/%d/%Y, %I:%M:%S")

def display_startup_banner():
    """Display a beautiful startup banner with loading indicator"""
    console.clear()
    
    # Show initial loading message
    loading_panel = Panel.fit(
        "[bold yellow]🚀 Auto-Swiper v2.0[/bold yellow]\n"
        "[cyan]Loading application...[/cyan]\n"
        "[dim]Please wait while we prepare everything for you[/dim]",
        box=box.DOUBLE,
        border_style="yellow"
    )
    console.print(loading_panel)
    
    # Simulate loading with progress bar
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        console=console,
        transient=True
    ) as progress:
        task = progress.add_task("Loading resources...", total=100)
        
        for i in range(100):
            time.sleep(0.02)  # Small delay for visual effect
            progress.update(task, advance=1)
    
    # Clear and show final banner
    console.clear()
    banner = Panel.fit(
        "[bold blue]🚀 Auto-Swiper v2.0[/bold blue]\n"
        "[cyan]Enhanced with Rich for beautiful terminal output[/cyan]\n"
        f"[green]Started: {s}[/green]\n"
        f"[dim]Custom jokes: ~/Documents/AutoSwiper_CustomJokes.txt[/dim]",
        box=box.DOUBLE,
        border_style="blue"
    )
    console.print(banner)
    console.print()

def getStartTime():
    return ("Start Date & Time = " + str(s))

def getEndTime():
    e = datetime.now().strftime("%m/%d/%Y, %I:%M:%S")
    return ("End Date & Time = " + str(e))

dividerBig = "=" * 100
divider = "-" * 50

defaultWaitTimeSecs = 3
pyautogui.FAILSAFE = True

def defaultLoc():
    pyautogui.moveTo(100, 150)

def wait(x):
    """Enhanced wait function without nested progress bars"""
    console.print(f"[cyan]⏳[/cyan] Waiting [yellow]{x}[/yellow] seconds...")
    time.sleep(x)

def clickFromLocation(ImagePath):
    """Enhanced click function with Rich status messages and debugging"""
    global imgCounter, skipCounter
    
    try:
        # Debug: Check if file exists before trying to locate
        if not os.path.exists(ImagePath):
            console.print(f"[red]❌[/red] File not found: [yellow]{ImagePath}[/yellow]")
            skipCounter += 1
            return
            
        console.print(f"[cyan]🔍[/cyan] Looking for image: [blue]{ImagePath}[/blue]")
        x, y = pyautogui.locateCenterOnScreen(ImagePath, grayscale=True, confidence=0.5)
        pyautogui.click(x, y)
        console.print(f"[green]✓[/green] Clicked on image: [blue]{ImagePath}[/blue]")
        imgCounter += 1
    except Exception as e:
        console.print(f"[yellow]⚠[/yellow] Skipped - couldn't find on screen: [red]{os.path.basename(ImagePath)}[/red]")
        # For debugging, show the exception type
        console.print(f"[dim]Debug: {type(e).__name__}: {str(e)[:100]}[/dim]")
        skipCounter += 1

def scroll(Pixels):
    """Enhanced scroll function with Rich output"""
    pyautogui.scroll(Pixels)
    console.print(f"[blue]📜[/blue] Scrolled [cyan]{Pixels}[/cyan] pixels")

def typeMessage(MessageString):
    pyautogui.typewrite(MessageString, interval=0.01)

def get_user_jokes_path():
    """Get path to user's custom jokes file"""
    import os
    from pathlib import Path
    
    # Use user's Documents folder for easy access
    if sys.platform == "win32":
        docs_path = Path.home() / "Documents"
    elif sys.platform == "darwin":  # macOS
        docs_path = Path.home() / "Documents"
    else:  # Linux
        docs_path = Path.home() / "Documents"
    
    return docs_path / "AutoSwiper_CustomJokes.txt"

def create_default_user_jokes():
    """Create a default custom jokes file for the user"""
    user_jokes_path = get_user_jokes_path()
    
    if not user_jokes_path.exists():
        default_custom_jokes = [
            "# AutoSwiper Custom Jokes",
            "# Edit this file to add your own pickup lines and messages!",
            "# Each line is a separate message (lines starting with # are ignored)",
            "",
            "Hey there! You seem awesome 😊",
            "Your smile is absolutely stunning!",
            "I'd love to get to know you better",
            "Coffee date? ☕",
            "You caught my eye immediately",
            "What's your favorite way to spend weekends?",
            "Your profile made me smile 😄",
            "Adventure buddy wanted! 🌟",
            "",
            "# Add your own lines below:",
            "# (Remove the # to activate them)",
            "# Your custom message here",
            "# Another custom message",
        ]
        
        try:
            user_jokes_path.parent.mkdir(exist_ok=True)
            with open(user_jokes_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(default_custom_jokes))
            console.print(f"[green]✨[/green] Created custom jokes file: [blue]{user_jokes_path}[/blue]")
            console.print(f"[cyan]💡[/cyan] Edit this file to add your own pickup lines!")
            return True
        except Exception as e:
            console.print(f"[yellow]⚠[/yellow] Couldn't create custom jokes file: {e}")
            return False
    return False

def loadJokes(filename):
    """Enhanced joke loading with user customization support"""
    jokes = []
    
    # 1. First, try to load user's custom jokes
    user_jokes_path = get_user_jokes_path()
    user_jokes_loaded = False
    
    if user_jokes_path.exists():
        try:
            with open(user_jokes_path, 'r', encoding='utf-8') as file:
                user_lines = file.read().splitlines()
                # Filter out comments and empty lines
                user_jokes = [line.strip() for line in user_lines 
                             if line.strip() and not line.strip().startswith('#')]
                if user_jokes:
                    jokes.extend(user_jokes)
                    user_jokes_loaded = True
                    console.print(f"[green]🎨[/green] Loaded [cyan]{len(user_jokes)}[/cyan] custom jokes from [blue]{user_jokes_path.name}[/blue]")
        except Exception as e:
            console.print(f"[yellow]⚠[/yellow] Error reading custom jokes: {e}")
    
    # 2. Load bundled default jokes as backup/supplement
    bundled_jokes_path = get_resource_path(filename)
    try:
        with open(bundled_jokes_path, 'r', encoding='utf-8') as file:
            default_jokes = file.read().splitlines()
            default_jokes = [joke.strip() for joke in default_jokes if joke.strip()]
            jokes.extend(default_jokes)
            console.print(f"[blue]📦[/blue] Loaded [cyan]{len(default_jokes)}[/cyan] default jokes")
    except Exception as e:
        console.print(f"[yellow]⚠[/yellow] Error reading bundled jokes: {e}")
    
    # 3. Create custom jokes file if it doesn't exist
    if not user_jokes_loaded:
        create_default_user_jokes()
    
    # 4. Fallback if no jokes loaded
    if not jokes:
        jokes = ["Hey there! 😊", "You seem interesting!", "Coffee sometime?"]
        console.print(f"[cyan]🔄[/cyan] Using fallback jokes")
    
    console.print(f"[green]✅[/green] Total active jokes: [bold cyan]{len(jokes)}[/bold cyan]")
    return jokes

def open_jokes_folder():
    """Open the folder containing the custom jokes file"""
    import subprocess
    import platform
    
    user_jokes_path = get_user_jokes_path()
    folder_path = user_jokes_path.parent
    
    try:
        if platform.system() == "Windows":
            subprocess.run(["explorer", str(folder_path)], check=True)
        elif platform.system() == "Darwin":  # macOS
            subprocess.run(["open", str(folder_path)], check=True)
        else:  # Linux
            subprocess.run(["xdg-open", str(folder_path)], check=True)
        console.print(f"[green]📂[/green] Opened jokes folder: [blue]{folder_path}[/blue]")
    except Exception as e:
        console.print(f"[yellow]⚠[/yellow] Could not open folder. Path: [blue]{user_jokes_path}[/blue]")

def randomPunGenerator(jokes):
    return random.choice(jokes) if jokes else "No jokes available"

def sequence(jokes):
    """Enhanced sequence with Rich message display"""
    defaultLoc()
    clickFromLocation(heartImg)
    wait(defaultWaitTimeSecs)
    clickFromLocation(commentImg)
    wait(defaultWaitTimeSecs)
    msg = randomPunGenerator(jokes)
    
    # Display joke in a beautiful panel
    joke_panel = Panel(
        Text(msg, style="italic cyan"),
        title="[bold blue]💬 Random Message[/bold blue]",
        border_style="cyan",
        box=box.ROUNDED
    )
    console.print(joke_panel)
    
    typeMessage(msg)
    wait(defaultWaitTimeSecs)
    clickFromLocation(likeImg)
    wait(defaultWaitTimeSecs)

def logAll():
    """Enhanced logging with Rich table display"""
    try:
        # Create a beautiful statistics table
        stats_table = Table(title="[bold blue]📊 Session Statistics[/bold blue]", box=box.ROUNDED)
        stats_table.add_column("Metric", style="cyan", no_wrap=True)
        stats_table.add_column("Count", style="green", justify="right")
        stats_table.add_column("Percentage", style="yellow", justify="right")
        
        total = imgCounter + skipCounter
        success_rate = (imgCounter / total * 100) if total > 0 else 0
        skip_rate = (skipCounter / total * 100) if total > 0 else 0
        
        stats_table.add_row("✅ Successful Clicks", str(imgCounter), f"{success_rate:.1f}%")
        stats_table.add_row("⚠️  Skipped Images", str(skipCounter), f"{skip_rate:.1f}%")
        stats_table.add_row("📈 Total Attempts", str(total), "100.0%")
        
        console.print(stats_table)
        
        # Write to log file (keep original format for compatibility)
        with open("log.txt", "a") as logFile:
            printSkip = f"Skipped Images = {skipCounter} Images"
            printComplete = f"Completed Images = {imgCounter} Images"
            printTotal = f"Total Images = {imgCounter + skipCounter} Images"
            log = (
                f"\n\n{dividerBig}\n{getStartTime()}\n{divider}\n{printSkip}\n{printComplete}\n"
                f"{printTotal}\n{divider}\n{getEndTime()}\n{dividerBig}\n\n"
            )
            logFile.write(log)
            
    except Exception as e:
        console.print(f"[red]❌[/red] Error writing to log file: [yellow]{e}[/yellow]")

def looper():
    """Enhanced main loop with Rich progress tracking"""
    global counter
    
    # Display startup banner
    display_startup_banner()
    
    jokes = loadJokes('jokes.txt')
    
    # Create overall progress tracking
    with Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TextColumn("({task.completed}/{task.total})"),
        TimeElapsedColumn(),
        console=console
    ) as overall_progress:
        
        main_task = overall_progress.add_task("[green]Overall Progress", total=200)
        
        while counter < 200:
            try:
                counter += 1
                
                # Display current like number with rich formatting
                like_text = Text(f"❤️  Like #{counter}", style="bold red")
                console.print(like_text)
                console.print()
                
                sequence(jokes)
                
                # Update progress
                overall_progress.update(main_task, advance=1)
                
                # Add some spacing
                console.print("─" * 50, style="dim")
                console.print()
                
            except KeyboardInterrupt:
                console.print("\n[yellow]⚠️  Process interrupted by user[/yellow]")
                break
            finally:
                logAll()
    
    # Final summary
    final_panel = Panel(
        f"[bold green]🎉 Session Complete![/bold green]\n"
        f"[cyan]Total likes attempted: {counter}[/cyan]\n"
        f"[green]Successful clicks: {imgCounter}[/green]\n"
        f"[yellow]Skipped images: {skipCounter}[/yellow]",
        title="[bold blue]📋 Final Summary[/bold blue]",
        border_style="green",
        box=box.DOUBLE
    )
    console.print(final_panel)

def demo_rich_features():
    """Demo function to showcase Rich enhancements without running automation"""
    console.print("\n[bold yellow]🎭 Rich Enhancement Demo Mode[/bold yellow]")
    console.print("[dim]Showcasing the beautiful terminal features...[/dim]\n")
    
    # Demo startup banner
    display_startup_banner()
    
    # Demo progress bar
    console.print("[cyan]Demo: Wait function with progress bar[/cyan]")
    wait(3)
    
    # Demo status messages
    console.print("[cyan]Demo: Status messages[/cyan]")
    console.print("[green]✓[/green] Simulated successful click on: [blue]Images/1_HEART.png[/blue]")
    console.print("[yellow]⚠[/yellow] Simulated skip - couldn't find: [red]Images/missing.png[/red]")
    
    # Demo joke panel
    joke_panel = Panel(
        Text("Why don't scientists trust atoms? Because they make up everything!", style="italic cyan"),
        title="[bold blue]💬 Random Message[/bold blue]",
        border_style="cyan",
        box=box.ROUNDED
    )
    console.print(joke_panel)
    
    # Demo statistics table
    stats_table = Table(title="[bold blue]📊 Demo Statistics[/bold blue]", box=box.ROUNDED)
    stats_table.add_column("Metric", style="cyan", no_wrap=True)
    stats_table.add_column("Count", style="green", justify="right")
    stats_table.add_column("Percentage", style="yellow", justify="right")
    
    stats_table.add_row("✅ Successful Clicks", "25", "83.3%")
    stats_table.add_row("⚠️  Skipped Images", "5", "16.7%")
    stats_table.add_row("📈 Total Attempts", "30", "100.0%")
    
    console.print(stats_table)
    
    # Demo final summary
    final_panel = Panel(
        "[bold green]🎉 Demo Complete![/bold green]\n"
        "[cyan]Rich enhancements are working perfectly![/cyan]\n"
        "[yellow]Run with 'python main.py' for full automation[/yellow]",
        title="[bold blue]📋 Demo Summary[/bold blue]",
        border_style="green",
        box=box.DOUBLE
    )
    console.print(final_panel)

def show_help():
    """Show help information"""
    help_panel = Panel.fit(
        "[bold blue]🚀 Auto-Swiper v2.0 - Help[/bold blue]\n\n"
        "[cyan]Usage:[/cyan]\n"
        "  [white]AutoSwiper[/white]              Start the auto-swiping\n"
        "  [white]AutoSwiper --jokes[/white]      Open custom jokes folder\n"
        "  [white]AutoSwiper --demo[/white]       Show Rich features demo\n"
        "  [white]AutoSwiper --help[/white]       Show this help\n\n"
        "[yellow]📝 Customizing Messages:[/yellow]\n"
        "  • Edit: [blue]~/Documents/AutoSwiper_CustomJokes.txt[/blue]\n"
        "  • Add your own pickup lines (one per line)\n"
        "  • Lines starting with # are comments\n"
        "  • App will create the file automatically\n\n"
        "[green]💡 Tips:[/green]\n"
        "  • Make sure Hinge is open before starting\n"
        "  • Position Bluestacks/emulator properly\n"
        "  • Press Ctrl+C to stop anytime",
        box=box.DOUBLE,
        border_style="blue"
    )
    console.print(help_panel)

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        if arg == "--demo":
            demo_rich_features()
        elif arg in ["--jokes", "--edit", "--customize"]:
            console.print("[yellow]📂[/yellow] Opening custom jokes folder...")
            create_default_user_jokes()  # Ensure file exists
            open_jokes_folder()
        elif arg in ["--help", "-h", "help"]:
            show_help()
        else:
            console.print(f"[red]❌[/red] Unknown argument: {sys.argv[1]}")
            show_help()
    else:
        looper()
