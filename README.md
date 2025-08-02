# Auto-Swiper

Automate swiping on Hinge using Bluestacks or any Android emulator.

![Auto-Swiper](logo.png)

## 📥 **Download**

> **✨ [**Download Latest Release**](../../releases/latest) - ready-to-use executables, no Python installation required!**

**Quick Links:**
- **[Latest Release Downloads](../../releases/latest)** - Stable executables
- **[All Releases](../../releases)** - Version history  
- **[Latest Build Artifacts](../../actions/workflows/build.yml)** - Cutting-edge builds

---

## Table of Contents

- [📥 Download](#-download)
- [🚀 Quick Start](#-quick-start)
- [🎨 Personalizing Your Messages](#-personalizing-your-messages)
- [✨ Features](#-features)
- [🛠️ Development Setup](#️-development-setup)
- [📦 Building & Distribution](#-building--distribution)
- [📁 Project Structure](#-project-structure)
- [🤝 Contributing](#-contributing)
- [⚖️ License & Disclaimer](#️-license--disclaimer)

## 🚀 Quick Start

### Option 1: Download Standalone Executable (Recommended)

1. **Download** your platform's executable from [**Latest Release**](../../releases/latest)
2. **Run** the executable directly:
   - **Windows**: Double-click `AutoSwiper.exe`
   - **macOS**: Right-click `AutoSwiper-macOS` → "Open" (bypass security warning)
   - **Linux**: `chmod +x AutoSwiper-Linux && ./AutoSwiper-Linux`

### Option 2: Run from Source

```bash
# Clone the repository
git clone https://github.com/yourusername/auto-swiper.git
cd auto-swiper

# Install uv (blazingly fast package manager)
curl -LsSf https://astral.sh/uv/install.sh | sh  # Unix/macOS
# Or on Windows: powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies with uv (much faster than pip!)
uv pip install -r requirements.txt

# Run the application
python main.py
```

## 🎨 Personalizing Your Messages

**Auto-Swiper lets you completely customize the pickup lines and messages it sends!**

### 📝 How to Add Your Own Messages

1. **Automatic Setup**: The first time you run Auto-Swiper, it creates a custom jokes file
2. **Easy Editing**: Find the file at `~/Documents/AutoSwiper_CustomJokes.txt`
3. **Quick Access**: Run `AutoSwiper --jokes` to open the folder instantly

### 📂 Opening Your Custom File

```bash
# Open the jokes folder directly
AutoSwiper --jokes

# Or navigate manually to:
# Windows: C:\Users\YourName\Documents\AutoSwiper_CustomJokes.txt
# macOS: ~/Documents/AutoSwiper_CustomJokes.txt  
# Linux: ~/Documents/AutoSwiper_CustomJokes.txt
```

### ✏️ Editing Your Messages

The custom file includes helpful examples and instructions:

```
# AutoSwiper Custom Jokes
# Edit this file to add your own pickup lines and messages!
# Each line is a separate message (lines starting with # are ignored)

Hey there! You seem awesome 😊
Your smile is absolutely stunning!
Coffee date? ☕
What's your favorite way to spend weekends?

# Add your own lines below:
# (Remove the # to activate them)
# Your custom message here
```

### 💡 Tips for Great Messages

- **Be authentic** - write in your own voice
- **Ask questions** - show genuine interest  
- **Keep it light** - humor works well
- **Be respectful** - always be kind and considerate
- **Use emojis** - they add personality (but don't overdo it)

---

## ✨ Features

- **🎯 Automated Swiping**: Automatically like profiles on Hinge
- **💬 Custom Messages**: Fully customizable pickup lines and messages 
- **🎨 Easy Personalization**: Edit your own jokes in a simple text file
- **📊 Beautiful Terminal UI**: Enhanced with Rich library for gorgeous output
- **📈 Real-time Progress**: Live progress bars and statistics tables
- **🌈 Colorful Status**: Rich colors and emojis for better visual feedback
- **📋 Smart Logging**: Beautiful terminal tables plus traditional log files
- **🔄 Error Resilience**: Continues operation even if UI elements aren't found
- **⚡ Loading Screen**: Beautiful startup animation while app initializes
- **⚡ Standalone Distribution**: No Python installation required for end users
- **🌍 Cross-Platform**: Works on Windows, macOS, and Linux

## 🛠️ Development Setup

### Prerequisites
- Python 3.8 or higher
- Bluestacks or any Android emulator with Hinge installed
- Virtual environment (recommended)

### Installation
```bash
# Clone and setup
git clone https://github.com/yourusername/auto-swiper.git
cd auto-swiper

# Virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Dependencies (with blazingly fast uv!)
uv pip install -r requirements.txt
uv pip install pyinstaller  # For building executables

# Test the enhanced application
python main.py

# You'll see beautiful Rich terminal output with:
# - Startup banner with colors and borders
# - Progress bars for waiting periods  
# - Colorful status messages for clicks
# - Beautiful panels for joke display
# - Statistics tables for session summary
```

## 📦 Building & Distribution

### Quick Build
```bash
# Build for current platform
python scripts/build_01_quick.py

# Cross-platform build
python scripts/build_03_cross_platform.py

# Optimized build (smaller size)
python scripts/build_02_optimized.py --build

# Clean build artifacts
python scripts/maint_cleanup.py
```

### Automated GitHub Releases
```bash
# Create release with automated builds for all platforms
git tag v1.0.0
git push origin v1.0.0
# GitHub Actions automatically builds Windows, macOS, and Linux executables
```

### Distribution Options

**PyInstaller (Current)**
- ✅ Single executable file (~54MB)
- ✅ All dependencies bundled
- ✅ No Python required for users
- ✅ Cross-platform support

**Alternative Options**
- **Briefcase**: Modern BeeWare tool for native installers
- **Nuitka**: Compiles to C++ for faster execution
- **cx_Freeze**: Alternative packaging solution

### Build Results
- **Windows**: `AutoSwiper-Windows.exe`
- **macOS**: `AutoSwiper-macOS` 
- **Linux**: `AutoSwiper-Linux`

## 📁 Project Structure

```
📁 auto-swiper/
├── 📁 Images/                          # PyAutoGUI recognition patterns
│   ├── 0_CHECK_FOR_LOADING.png
│   ├── 0_CHECK_FOR_ROSE.png
│   ├── 1_HEART.png
│   ├── 2_ADD_COMMENT.png
│   ├── 3_SEND_LIKE.png
│   └── 4_RANDOM_X.png
├── 📁 scripts/                         # Build and automation tools
│   ├── build_01_quick.py               # Fast development builds
│   ├── build_02_optimized.py           # Production builds
│   ├── build_03_cross_platform.py      # Multi-platform setup
│   ├── build_manager.py                # Build orchestrator
│   └── maint_cleanup.py                # Clean build artifacts
├── 📁 .github/workflows/               # CI/CD automation
│   └── build.yml                       # Cross-platform builds
├── main.py                             # Core application with Rich UI
├── jokes.txt                           # Random interaction messages
├── requirements.txt                    # Python dependencies
├── LICENSE.md                          # Apache 2.0 license
└── README.md                           # This file
```

### Core Components
- **`main.py`**: Enhanced automation with Rich UI, image recognition, logging system
- **`Images/`**: PyAutoGUI recognition patterns for UI elements  
- **`scripts/`**: Modern build tools and automation utilities (2025 Edition)
- **`.github/workflows/`**: Automated CI/CD for cross-platform releases

### 🚀 **Modern Build System (2025 Edition)**

**Single Command Interface:**
```bash
# Quick development build
python scripts/build_manager.py quick

# Production-optimized build  
python scripts/build_manager.py optimized

# Cross-platform CI/CD setup
python scripts/build_manager.py cross

# Analyze dependencies and size
python scripts/build_manager.py analysis
```

**Advanced Features:**
- **🔥 Python 3.11+ Optimizations**: 10-15% faster execution + advanced features
- **⚡ uv Integration**: Lightning-fast dependency management  
- **🎨 Rich UI**: Beautiful terminal output with progress bars and status tables
- **🛡️ Smart Error Handling**: Comprehensive validation and helpful error messages
- **📊 Build Analytics**: Size analysis, timing, and optimization recommendations
- **🌍 Platform Detection**: Automatic platform-specific optimizations

**Individual Scripts** (for specific needs):
```bash
python scripts/build_01_quick.py --console      # Quick build with console
python scripts/build_02_optimized.py --build # Size-optimized build
python scripts/build_03_cross_platform.py    # GitHub Actions setup
python scripts/maint_cleanup.py              # Clean build artifacts
```

### ✨ Enhanced Terminal Experience
The script now features:
- **🎨 Beautiful Startup Banner**: Colorful welcome message with project info
- **📊 Live Progress Bars**: Real-time progress during waiting periods
- **🎯 Status Messages**: Color-coded success/error messages with emojis
- **💬 Message Panels**: Elegant display of random jokes/messages
- **📈 Statistics Tables**: Beautiful tables showing session statistics
- **🎉 Final Summary**: Comprehensive end-of-session report

## 🤝 Contributing

We welcome contributions! Here's how to get started:

### Development Process
1. **Fork and Clone**:
   ```bash
   git clone https://github.com/your-username/auto-swiper.git
   cd auto-swiper
   ```

2. **Set up Environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   uv pip install -r requirements.txt
   uv pip install pyinstaller
   ```

3. **Test Your Changes**:
   ```bash
   python main.py              # Test the application
   python scripts/build_01_quick.py     # Test building executable
   ```

### Contribution Areas
- **🎨 UI Improvements**: Better console output or interface
- **⚡ Build Optimization**: Reduce executable size
- **🌍 Cross-Platform**: Improve compatibility
- **🔒 Security**: Code signing, antivirus compatibility
- **📖 Documentation**: Improve guides and examples

### Code Standards
- Follow PEP 8 for Python code style
- Add comments for complex automation logic
- Test on multiple platforms when possible
- Update documentation for new features

### Bug Reports
Include:
- Operating system and version
- Python version (if running from source)
- Steps to reproduce
- Error messages or logs
- Screenshots if applicable

## ⚖️ License & Disclaimer

### License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

### Disclaimer
**⚠️ Educational Use Only**

This software is intended for educational and personal use only. Use of this software to automate interactions on third-party platforms, such as Hinge and Bluestacks, may violate their terms of service. The author does not condone or encourage any activities that violate the terms of service of any platform.

Users are responsible for their own actions when using this software. The author assumes no liability for any misuse of this software or any consequences resulting from its use.

### Security Notes
- Antivirus software may flag executables as false positives
- Consider code signing for production releases
- Grant accessibility permissions when prompted (macOS/Linux)

---

## 🎊 Success!

Your Auto-Swiper is now a **professional, distributable application**! 

- ✅ **Users**: Download and run executable - no technical setup needed
- ✅ **Developers**: Full build system with automated releases
- ✅ **Maintainers**: Clean structure with comprehensive documentation

**Questions?** Feel free to open an issue or contact: parth.chandak02@gmail.com

**Happy Swiping!** 🚀
