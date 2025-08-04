"""
Main entry point for Python Automation Suite
"""
import sys
import os
import file_organizer
import batch_renamer
import time_tracker
import system_monitor

def print_menu():
    print("\n🤖 Python Automation Suite")
    print("=" * 40)
    print("1. 📁 Intelligent file organizer")
    print("2. 🔄 Batch file renamer")
    print("3. ↶ Undo last rename")
    print("4. 📋 View rename history")
    print("5. ⏱️ Time tracking utilities")
    print("6. 📊 System monitoring")
    print("7. 🖥️ Launch GUI Version")
    print("0. ❌ Exit")
    print("=" * 40)

def main():
    print("🚀 Welcome to Python Automation Suite!")
    print("Choose your interface:")
    print("1. GUI (Recommended)")
    print("2. Command Line Interface")
    
    choice = input("\nSelect interface (1 or 2): ").strip()
    
    if choice == '1':
        try:
            import gui_main
            print("🖥️ Launching GUI...")
            gui_main.main()
        except ImportError as e:
            print(f"❌ Error launching GUI: {e}")
            print("Falling back to CLI...")
            run_cli()
    elif choice == '2':
        run_cli()
    else:
        print("Invalid choice. Launching GUI by default...")
        try:
            import gui_main
            gui_main.main()
        except ImportError:
            run_cli()

def run_cli():
    """Run the command line interface"""
    while True:
        print_menu()
        choice = input("\nSelect an option: ").strip()
        
        if choice == '1':
            directory = input("📁 Enter directory to organize: ").strip()
            if directory:
                file_organizer.organize_files_by_extension(directory)
            else:
                print("❌ No directory specified!")
                
        elif choice == '2':
            directory = input("📁 Enter directory to rename files: ").strip()
            prefix = input("🏷️ Enter prefix for files: ").strip()
            if directory and prefix:
                success = batch_renamer.batch_rename(directory, prefix)
                if success:
                    undo_choice = input("\n❓ Would you like to undo this operation? (y/n): ").strip().lower()
                    if undo_choice == 'y':
                        batch_renamer.undo_last_rename()
            else:
                print("❌ Please provide both directory and prefix!")
                
        elif choice == '3':
            print("↶ Undoing last rename operation...")
            batch_renamer.undo_last_rename()
            
        elif choice == '4':
            print("📋 Rename History:")
            batch_renamer.list_rename_history()
            if batch_renamer.rename_history:
                undo_choice = input("\n❓ Enter session number to undo (or press Enter to skip): ").strip()
                if undo_choice.isdigit():
                    session_num = int(undo_choice)
                    if 0 <= session_num < len(batch_renamer.rename_history):
                        batch_renamer.undo_rename_session(session_num)
                    else:
                        print("❌ Invalid session number!")
                        
        elif choice == '5':
            tracker = time_tracker.TimeTracker()
            tracker.start()
            input("⏱️ Press Enter to stop timer...")
            tracker.stop()
            
        elif choice == '6':
            print("📊 System Statistics:")
            print("-" * 30)
            system_monitor.show_system_stats()
            
        elif choice == '7':
            try:
                import gui_main
                print("🖥️ Launching GUI...")
                gui_main.main()
                break
            except ImportError as e:
                print(f"❌ Error launching GUI: {e}")
                
        elif choice == '0':
            print("👋 Goodbye!")
            sys.exit(0)
        else:
            print("❌ Invalid option. Please try again.")

if __name__ == "__main__":
    main()
