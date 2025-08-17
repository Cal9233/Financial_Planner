#!/usr/bin/env python3
"""
Main.py - Marine Rental Company Management System
Entry point for the GUI application
"""

import sys
import os

# Add the current directory to the Python path to ensure imports work
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from GUI import MRCGUIApplication
    import tkinter as tk
    from tkinter import messagebox
except ImportError as e:
    print(f"Import Error: {e}")
    print("Please ensure all required packages are installed:")
    print("- tkinter (usually comes with Python)")
    print("- tkcalendar (pip install tkcalendar)")
    print("- mysql-connector-python (pip install mysql-connector-python)")
    sys.exit(1)

def check_dependencies():
    """Check if all required dependencies are available"""
    try:
        import mysql.connector
        import tkcalendar
        return True
    except ImportError as e:
        error_msg = f"Missing dependency: {e}\n\n"
        error_msg += "Please install the required packages:\n"
        error_msg += "pip install mysql-connector-python tkcalendar"
        
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        messagebox.showerror("Dependency Error", error_msg)
        root.destroy()
        return False

def main():
    """Main application entry point"""
    print("Marine Rental Company Management System")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        print("Error: Missing required dependencies")
        return 1
    
    try:
        # Create and run the GUI application
        app = MRCGUIApplication()
        app.run()
        return 0
        
    except Exception as e:
        error_msg = f"Application Error: {str(e)}"
        print(error_msg)
        
        # Try to show error in GUI if possible
        try:
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("Application Error", error_msg)
            root.destroy()
        except:
            pass
        
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)