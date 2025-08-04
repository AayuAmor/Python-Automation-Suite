"""
Direct GUI Launcher for Python Automation Suite
Double-click this file to launch the GUI directly
"""
import tkinter as tk
from tkinter import messagebox
import sys
import os

try:
    import gui_main
    gui_main.main()
except ImportError as e:
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    messagebox.showerror("Missing Dependencies", 
                        f"Error: {e}\n\nPlease ensure all required modules are installed.")
    sys.exit(1)
except Exception as e:
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror("Error", f"An error occurred: {e}")
    sys.exit(1)
