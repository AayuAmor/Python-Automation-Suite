"""
GUI Main entry point for Python Automation Suite
Modern graphical interface using tkinter
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import os
import file_organizer
import batch_renamer
import time_tracker
import system_monitor

class AutomationSuiteGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🤖 Python Automation Suite")
        self.root.geometry("800x600")
        self.root.configure(bg='#2b2b2b')
        
        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.configure_styles()
        
        # Initialize timer
        self.timer = None
        self.timer_running = False
        
        self.create_widgets()
        
    def configure_styles(self):
        # Configure custom styles
        self.style.configure('Title.TLabel', 
                           font=('Arial', 16, 'bold'),
                           background='#2b2b2b',
                           foreground='#ffffff')
        
        self.style.configure('Header.TLabel',
                           font=('Arial', 12, 'bold'),
                           background='#2b2b2b',
                           foreground='#4CAF50')
        
        self.style.configure('Custom.TButton',
                           font=('Arial', 10),
                           padding=10)
        
    def create_widgets(self):
        # Main title
        title_label = ttk.Label(self.root, text="🤖 Python Automation Suite", style='Title.TLabel')
        title_label.pack(pady=20)
        
        # Status bar (create this first so status_var exists)
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, 
                              relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X, pady=(0, 5))
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Create tabs
        self.create_file_organizer_tab()
        self.create_batch_renamer_tab()
        self.create_time_tracker_tab()
        self.create_system_monitor_tab()
        
    def create_file_organizer_tab(self):
        # File Organizer Tab
        organizer_frame = ttk.Frame(self.notebook)
        self.notebook.add(organizer_frame, text="📁 File Organizer")
        
        ttk.Label(organizer_frame, text="Intelligent File Organizer", 
                 style='Header.TLabel').pack(pady=10)
        
        ttk.Label(organizer_frame, text="Select a directory to organize files by extension:").pack(pady=5)
        
        # Directory selection frame
        dir_frame = ttk.Frame(organizer_frame)
        dir_frame.pack(pady=10, fill='x', padx=20)
        
        self.org_dir_var = tk.StringVar()
        ttk.Entry(dir_frame, textvariable=self.org_dir_var, width=60).pack(side='left', padx=(0, 10))
        ttk.Button(dir_frame, text="Browse", command=self.browse_organize_directory).pack(side='left')
        
        ttk.Button(organizer_frame, text="🗂️ Organize Files", 
                  style='Custom.TButton',
                  command=self.organize_files).pack(pady=20)
        
        # Output text area
        self.org_output = scrolledtext.ScrolledText(organizer_frame, height=8, width=70)
        self.org_output.pack(pady=10, padx=20, fill='both', expand=True)
