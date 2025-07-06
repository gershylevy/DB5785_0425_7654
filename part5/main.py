
# main.py - Main Application Entry Point
"""
Customer Database Management System
Main application entry point
"""
import tkinter as tk
from gui.main_app import CustomerDatabaseGUI

def main():
    """Main function to run the application"""
    try:
        root = tk.Tk()
        app = CustomerDatabaseGUI(root)
        root.mainloop()
    except Exception as e:
        print(f"Error starting application: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
