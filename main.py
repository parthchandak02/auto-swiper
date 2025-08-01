import pyautogui
import time
from datetime import datetime
import random

# Rich imports for beautiful terminal output
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.live import Live
from rich import box

# Initialize Rich console
console = Console()

# Image paths
roseCheckImg = 'Images/0_CHECK_FOR_ROSE.png'
heartImg = 'Images/1_HEART.png'
commentImg = 'Images/2_ADD_COMMENT.png'
likeImg = 'Images/3_SEND_LIKE.png'

# Counters
counter = 0
imgCounter = 0
skipCounter = 0

# Start time
s = datetime.now().strftime("%m/%d/%Y, %I:%M:%S")

def display_startup_banner():
    """Display a beautiful startup banner"""
    banner = Panel.fit(
        "[bold blue]🚀 Auto-Swiper v2.0[/bold blue]\n"
        "[cyan]Enhanced with Rich for beautiful terminal output[/cyan]\n"
        f"[green]Started: {s}[/green]",
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
    """Enhanced wait function with Rich progress bar"""
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeElapsedColumn(),
        console=console,
        transient=True  # Progress bar disappears after completion
    ) as progress:
        task = progress.add_task(f"[cyan]Waiting {x} seconds...", total=x)
        for i in range(x):
            time.sleep(1)
            progress.update(task, advance=1)

def clickFromLocation(ImagePath):
    """Enhanced click function with Rich status messages"""
    try:
        x, y = pyautogui.locateCenterOnScreen(ImagePath, grayscale=True, confidence=0.5)
        pyautogui.click(x, y)
        console.print(f"[green]✓[/green] Clicked on image: [blue]{ImagePath}[/blue]")
        global imgCounter
        imgCounter += 1
    except:
        console.print(f"[yellow]⚠[/yellow] Skipped - couldn't find: [red]{ImagePath}[/red]")
        global skipCounter
        skipCounter += 1

def scroll(Pixels):
    """Enhanced scroll function with Rich output"""
    pyautogui.scroll(Pixels)
    console.print(f"[blue]📜[/blue] Scrolled [cyan]{Pixels}[/cyan] pixels")

def typeMessage(MessageString):
    pyautogui.typewrite(MessageString, interval=0.01)

def loadJokes(filename):
    """Enhanced joke loading with Rich error handling"""
    try:
        with open(filename, 'r') as file:
            jokes = file.read().splitlines()
        console.print(f"[green]📝[/green] Loaded [cyan]{len(jokes)}[/cyan] jokes from [blue]{filename}[/blue]")
        return jokes
    except Exception as e:
        console.print(f"[red]❌[/red] Error reading jokes file: [yellow]{e}[/yellow]")
        return []

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

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        demo_rich_features()
    else:
        looper()
