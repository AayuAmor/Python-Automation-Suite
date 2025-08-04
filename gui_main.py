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
        
    def create_batch_renamer_tab(self):
        # Batch Renamer Tab
        renamer_frame = ttk.Frame(self.notebook)
        self.notebook.add(renamer_frame, text="🔄 Batch Renamer")
        
        ttk.Label(renamer_frame, text="Batch File Renamer with Undo", 
                 style='Header.TLabel').pack(pady=10)
        
        # Main controls frame
        controls_frame = ttk.Frame(renamer_frame)
        controls_frame.pack(fill='x', padx=20, pady=10)
        
        # Left side - Rename controls
        rename_frame = ttk.LabelFrame(controls_frame, text="Rename Files", padding=10)
        rename_frame.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        # Directory selection
        ttk.Label(rename_frame, text="Select directory with files to rename:").pack(pady=5, anchor='w')
        
        dir_frame = ttk.Frame(rename_frame)
        dir_frame.pack(pady=5, fill='x')
        
        self.rename_dir_var = tk.StringVar()
        ttk.Entry(dir_frame, textvariable=self.rename_dir_var, width=40).pack(side='left', fill='x', expand=True, padx=(0, 5))
        ttk.Button(dir_frame, text="Browse", command=self.browse_rename_directory).pack(side='right')
        
        # Prefix input
        prefix_frame = ttk.Frame(rename_frame)
        prefix_frame.pack(pady=5, fill='x')
        
        ttk.Label(prefix_frame, text="Prefix for renamed files:").pack(side='left')
        self.prefix_var = tk.StringVar(value="file")
        ttk.Entry(prefix_frame, textvariable=self.prefix_var, width=15).pack(side='right')
        
        ttk.Button(rename_frame, text="🏷️ Rename Files", 
                  style='Custom.TButton',
                  command=self.rename_files).pack(pady=10)
        
        # Right side - Undo controls
        undo_frame = ttk.LabelFrame(controls_frame, text="Undo Operations", padding=10)
        undo_frame.pack(side='right', fill='both', expand=True, padx=(10, 0))
        
        # Undo buttons
        ttk.Button(undo_frame, text="↶ Undo Last", 
                  style='Custom.TButton',
                  command=self.undo_last_rename).pack(pady=5, fill='x')
        
        ttk.Button(undo_frame, text="📋 View History", 
                  style='Custom.TButton',
                  command=self.show_rename_history).pack(pady=5, fill='x')
        
        ttk.Button(undo_frame, text="🗑️ Clear History", 
                  style='Custom.TButton',
                  command=self.clear_rename_history).pack(pady=5, fill='x')
        
        # History listbox
        ttk.Label(undo_frame, text="Recent Sessions:").pack(pady=(10, 5), anchor='w')
        
        history_frame = ttk.Frame(undo_frame)
        history_frame.pack(fill='both', expand=True)
        
        self.history_listbox = tk.Listbox(history_frame, height=4, font=('Courier', 8))
        history_scrollbar = ttk.Scrollbar(history_frame, orient='vertical', command=self.history_listbox.yview)
        self.history_listbox.configure(yscrollcommand=history_scrollbar.set)
        
        self.history_listbox.pack(side='left', fill='both', expand=True)
        history_scrollbar.pack(side='right', fill='y')
        
        # Bind double-click to undo specific session
        self.history_listbox.bind('<Double-1>', self.undo_selected_session)
        
        ttk.Button(undo_frame, text="↶ Undo Selected", 
                  style='Custom.TButton',
                  command=lambda: self.undo_selected_session(None)).pack(pady=5, fill='x')
        
        # Output text area
        ttk.Label(renamer_frame, text="Output Log:").pack(pady=(20, 5), padx=20, anchor='w')
        self.rename_output = scrolledtext.ScrolledText(renamer_frame, height=8, width=70)
        self.rename_output.pack(pady=5, padx=20, fill='both', expand=True)
        
        # Load initial history
        self.refresh_rename_history()
        
    def create_time_tracker_tab(self):
        # Time Tracker Tab
        tracker_frame = ttk.Frame(self.notebook)
        self.notebook.add(tracker_frame, text="⏱️ Time Tracker")
        
        ttk.Label(tracker_frame, text="Time Tracking Utilities", 
                 style='Header.TLabel').pack(pady=10)
        
        # Timer display
        self.time_var = tk.StringVar(value="00:00:00")
        time_display = ttk.Label(tracker_frame, textvariable=self.time_var, 
                                font=('Arial', 24, 'bold'))
        time_display.pack(pady=20)
        
        # Timer buttons
        button_frame = ttk.Frame(tracker_frame)
        button_frame.pack(pady=20)
        
        self.start_btn = ttk.Button(button_frame, text="▶️ Start", 
                                   style='Custom.TButton',
                                   command=self.start_timer)
        self.start_btn.pack(side='left', padx=10)
        
        self.stop_btn = ttk.Button(button_frame, text="⏹️ Stop", 
                                  style='Custom.TButton',
                                  command=self.stop_timer, state='disabled')
        self.stop_btn.pack(side='left', padx=10)
        
        self.reset_btn = ttk.Button(button_frame, text="🔄 Reset", 
                                   style='Custom.TButton',
                                   command=self.reset_timer)
        self.reset_btn.pack(side='left', padx=10)
        
        # Timer log
        ttk.Label(tracker_frame, text="Timer Log:").pack(pady=(20, 5))
        self.timer_log = scrolledtext.ScrolledText(tracker_frame, height=10, width=70)
        self.timer_log.pack(pady=10, padx=20, fill='both', expand=True)
        
    def create_system_monitor_tab(self):
        # System Monitor Tab
        monitor_frame = ttk.Frame(self.notebook)
        self.notebook.add(monitor_frame, text="📊 System Monitor")
        
        ttk.Label(monitor_frame, text="System Monitoring", 
                 style='Header.TLabel').pack(pady=10)
        
        # Refresh button
        ttk.Button(monitor_frame, text="🔄 Refresh Stats", 
                  style='Custom.TButton',
                  command=self.refresh_system_stats).pack(pady=10)
        
        # System stats display
        self.stats_text = scrolledtext.ScrolledText(monitor_frame, height=15, width=70)
        self.stats_text.pack(pady=10, padx=20, fill='both', expand=True)
        
        # Auto-refresh checkbox
        self.auto_refresh_var = tk.BooleanVar()
        ttk.Checkbutton(monitor_frame, text="Auto-refresh every 5 seconds", 
                       variable=self.auto_refresh_var,
                       command=self.toggle_auto_refresh).pack(pady=10)
        
        # Load initial stats after the interface is ready
        self.root.after(100, self.refresh_system_stats)
        
    def browse_organize_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.org_dir_var.set(directory)
            
    def browse_rename_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.rename_dir_var.set(directory)
            
    def organize_files(self):
        directory = self.org_dir_var.get()
        if not directory:
            messagebox.showerror("Error", "Please select a directory first!")
            return
            
        self.org_output.delete(1.0, tk.END)
        self.status_var.set("Organizing files...")
        
        def organize_thread():
            try:
                # Capture output
                import io
                import sys
                old_stdout = sys.stdout
                sys.stdout = captured_output = io.StringIO()
                
                file_organizer.organize_files_by_extension(directory)
                
                sys.stdout = old_stdout
                output = captured_output.getvalue()
                
                self.root.after(0, lambda: self.org_output.insert(tk.END, output))
                self.root.after(0, lambda: self.status_var.set("Files organized successfully!"))
                
            except Exception as e:
                self.root.after(0, lambda: self.org_output.insert(tk.END, f"Error: {str(e)}"))
                self.root.after(0, lambda: self.status_var.set("Error occurred"))
                
        threading.Thread(target=organize_thread, daemon=True).start()
        
    def rename_files(self):
        directory = self.rename_dir_var.get()
        prefix = self.prefix_var.get()
        
        if not directory:
            messagebox.showerror("Error", "Please select a directory first!")
            return
        if not prefix:
            messagebox.showerror("Error", "Please enter a prefix!")
            return
            
        self.rename_output.delete(1.0, tk.END)
        self.status_var.set("Renaming files...")
        
        def rename_thread():
            try:
                import io
                import sys
                old_stdout = sys.stdout
                sys.stdout = captured_output = io.StringIO()
                
                batch_renamer.batch_rename(directory, prefix)
                
                sys.stdout = old_stdout
                output = captured_output.getvalue()
                
                self.root.after(0, lambda: self.rename_output.insert(tk.END, output))
                self.root.after(0, lambda: self.status_var.set("Files renamed successfully!"))
                
            except Exception as e:
                self.root.after(0, lambda: self.rename_output.insert(tk.END, f"Error: {str(e)}"))
                self.root.after(0, lambda: self.status_var.set("Error occurred"))
                
        threading.Thread(target=rename_thread, daemon=True).start()
        
        # Refresh history after rename
        self.root.after(2000, self.refresh_rename_history)
        
    def undo_last_rename(self):
        """Undo the most recent rename operation"""
        self.rename_output.delete(1.0, tk.END)
        self.status_var.set("Undoing last rename...")
        
        def undo_thread():
            try:
                import io
                import sys
                old_stdout = sys.stdout
                sys.stdout = captured_output = io.StringIO()
                
                success = batch_renamer.undo_last_rename()
                
                sys.stdout = old_stdout
                output = captured_output.getvalue()
                
                self.root.after(0, lambda: self.rename_output.insert(tk.END, output))
                if success:
                    self.root.after(0, lambda: self.status_var.set("Undo completed successfully!"))
                    self.root.after(100, self.refresh_rename_history)
                else:
                    self.root.after(0, lambda: self.status_var.set("Undo failed or nothing to undo"))
                
            except Exception as e:
                self.root.after(0, lambda: self.rename_output.insert(tk.END, f"Error: {str(e)}"))
                self.root.after(0, lambda: self.status_var.set("Error during undo"))
                
        threading.Thread(target=undo_thread, daemon=True).start()
        
    def undo_selected_session(self, event):
        """Undo a selected session from the history list"""
        selection = self.history_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a session to undo.")
            return
        
        session_index = len(batch_renamer.rename_history) - 1 - selection[0]  # Reverse index
        
        # Confirm undo
        if messagebox.askyesno("Confirm Undo", 
                              f"Are you sure you want to undo session #{session_index}?\n"
                              "This will restore the original file names."):
            
            self.rename_output.delete(1.0, tk.END)
            self.status_var.set(f"Undoing session #{session_index}...")
            
            def undo_thread():
                try:
                    import io
                    import sys
                    old_stdout = sys.stdout
                    sys.stdout = captured_output = io.StringIO()
                    
                    success = batch_renamer.undo_rename_session(session_index)
                    
                    sys.stdout = old_stdout
                    output = captured_output.getvalue()
                    
                    self.root.after(0, lambda: self.rename_output.insert(tk.END, output))
                    if success:
                        self.root.after(0, lambda: self.status_var.set("Session undo completed!"))
                        self.root.after(100, self.refresh_rename_history)
                    else:
                        self.root.after(0, lambda: self.status_var.set("Session undo failed"))
                    
                except Exception as e:
                    self.root.after(0, lambda: self.rename_output.insert(tk.END, f"Error: {str(e)}"))
                    self.root.after(0, lambda: self.status_var.set("Error during undo"))
                    
            threading.Thread(target=undo_thread, daemon=True).start()
        
    def show_rename_history(self):
        """Show detailed rename history in the output"""
        self.rename_output.delete(1.0, tk.END)
        self.status_var.set("Loading rename history...")
        
        def history_thread():
            try:
                import io
                import sys
                old_stdout = sys.stdout
                sys.stdout = captured_output = io.StringIO()
                
                batch_renamer.list_rename_history()
                
                sys.stdout = old_stdout
                output = captured_output.getvalue()
                
                self.root.after(0, lambda: self.rename_output.insert(tk.END, output))
                self.root.after(0, lambda: self.status_var.set("History loaded"))
                
            except Exception as e:
                self.root.after(0, lambda: self.rename_output.insert(tk.END, f"Error: {str(e)}"))
                self.root.after(0, lambda: self.status_var.set("Error loading history"))
                
        threading.Thread(target=history_thread, daemon=True).start()
        
    def clear_rename_history(self):
        """Clear all rename history after confirmation"""
        if messagebox.askyesno("Confirm Clear", 
                              "Are you sure you want to clear all rename history?\n"
                              "This action cannot be undone."):
            
            batch_renamer.clear_rename_history()
            self.refresh_rename_history()
            self.rename_output.delete(1.0, tk.END)
            self.rename_output.insert(tk.END, "✅ Rename history cleared.\n")
            self.status_var.set("History cleared")
            
    def refresh_rename_history(self):
        """Refresh the history listbox with current sessions"""
        self.history_listbox.delete(0, tk.END)
        
        # Load current history
        batch_renamer.load_rename_history()
        
        if not batch_renamer.rename_history:
            self.history_listbox.insert(0, "No history")
            return
        
        # Show most recent sessions first
        for i, session in enumerate(reversed(batch_renamer.rename_history)):
            timestamp = session['timestamp'][:19].replace('T', ' ')  # Format timestamp
            prefix = session['prefix']
            num_ops = len(session['operations'])
            
            entry = f"{timestamp} | {prefix} ({num_ops} files)"
            self.history_listbox.insert(tk.END, entry)
        
    def start_timer(self):
        if not self.timer_running:
            self.timer = time_tracker.TimeTracker()
            self.timer.start()
            self.timer_running = True
            self.start_btn.config(state='disabled')
            self.stop_btn.config(state='normal')
            self.update_timer_display()
            
    def stop_timer(self):
        if self.timer_running and self.timer:
            elapsed = self.timer.stop()
            self.timer_running = False
            self.start_btn.config(state='normal')
            self.stop_btn.config(state='disabled')
            
            # Log the session
            log_entry = f"Session completed: {elapsed:.2f} seconds\n"
            self.timer_log.insert(tk.END, log_entry)
            self.timer_log.see(tk.END)
            
    def reset_timer(self):
        self.time_var.set("00:00:00")
        if self.timer_running:
            self.stop_timer()
            
    def update_timer_display(self):
        if self.timer_running and self.timer:
            import time
            elapsed = time.time() - self.timer.start_time
            hours = int(elapsed // 3600)
            minutes = int((elapsed % 3600) // 60)
            seconds = int(elapsed % 60)
            
            time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
            self.time_var.set(time_str)
            
            self.root.after(1000, self.update_timer_display)
