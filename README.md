# 🤖 Python Automation Suite

Smart automation tools for daily tasks with both **GUI** and **CLI** interfaces!

## 🎨 User Interface Options

### 🖥️ Modern GUI Interface (Recommended)

- Beautiful tabbed interface
- Real-time timer with display
- File browser integration
- Progress feedback and status updates
- Auto-refresh system monitoring

### 💻 Command Line Interface

- Classic terminal-based interaction
- Quick access for power users
- Scriptable and automation-friendly

## Features

### 📁 Intelligent File Organizer

- Automatically organizes files in a directory by their extensions
- Creates subdirectories for each file type
- Handles files without extensions

### 🔄 Batch File Renamer

- Renames multiple files with a common prefix
- Adds sequential numbering (001, 002, etc.)
- Preserves file extensions

### ⏱️ Time Tracking Utilities

- Simple timer for tracking task duration
- Start/stop functionality
- Displays elapsed time in seconds

### 📊 System Monitoring

- Shows real-time CPU usage
- Displays memory usage percentage and available memory
- Shows disk usage and available space
- Cross-platform compatibility (Windows/Linux/Mac)

## Requirements

- Python 3.6+
- psutil package (automatically installed)

## 🚀 Quick Start

### Launch GUI (Recommended)

```bash
python gui_main.py
```

or double-click

```bash
python launch_gui.py
```

### Launch with Interface Choice

```bash
python main.py
```

### Direct CLI Access

```bash
python main.py
# Then select option 2 for CLI
```

## 📱 GUI Features

### 📁 File Organizer Tab

- Browse button for easy directory selection
- Real-time output display
- Progress feedback

### 🔄 Batch Renamer Tab

- Directory browser
- Customizable prefix input
- Live preview of operations

### ⏱️ Time Tracker Tab

- Large digital timer display
- Start/Stop/Reset buttons
- Session history log
- Real-time updates

### 📊 System Monitor Tab

- Real-time system statistics
- Auto-refresh option (every 5 seconds)
- CPU, Memory, and Disk usage
- Available space information

## 💻 CLI Usage

Run the main script and select from the menu options:

1. **File Organizer**: Enter a directory path to organize files by extension
2. **Batch Renamer**: Enter directory path and prefix to rename files
3. **Time Tracker**: Start/stop timer for time tracking
4. **System Monitor**: View current system statistics
5. **Launch GUI**: Switch to graphical interface
6. **Exit**: Close the application

## Example

```
Python Automation Suite
1. Intelligent file organizer
2. Batch file renamer
3. Time tracking utilities
4. System monitoring
0. Exit
Select an option: 1
Enter directory to organize: C:\Users\Downloads
Organized 15 files in C:\Users\Downloads by extension.
```

## Error Handling

The suite includes comprehensive error handling for:

- Invalid directory paths
- Empty directories
- Permission errors
- System monitoring failures

Enjoy automating your daily tasks! 🚀
This suite includes lightweight, intelligent utilities built with Python to simplify and automate everyday system operations and workflows.
