# launcher_fixed.py - Fixed launcher with better error handling
import tkinter as tk
from tkinter import messagebox, simpledialog
import sys
import os
import subprocess
import traceback

def check_dependencies():
    """Check if all required dependencies are installed"""
    required_packages = []
    
    # Check tkinter
    try:
        import tkinter
        print("✅ tkinter found")
    except ImportError:
        required_packages.append('tkinter')
        print("❌ tkinter missing")
    
    # Check psycopg2
    try:
        import psycopg2
        print("✅ psycopg2 found")
    except ImportError:
        required_packages.append('psycopg2')
        print("❌ psycopg2 missing")
    
    return required_packages

def check_database_files():
    """Check if database initialization files exist"""
    required_files = {
        'customer_db_gui.py': 'Main GUI application',
        'config.py': 'Database configuration (optional)',
        'db_utils.py': 'Database utilities (optional)'
    }
    
    missing_files = []
    for filename, description in required_files.items():
        if not os.path.exists(filename):
            missing_files.append((filename, description))
            print(f"❌ Missing: {filename}")
        else:
            print(f"✅ Found: {filename}")
    
    return missing_files

def test_tkinter():
    """Test if tkinter works properly"""
    try:
        print("Testing tkinter...")
        root = tk.Tk()
        root.withdraw()  # Hide the window
        root.destroy()
        print("✅ tkinter test successful")
        return True
    except Exception as e:
        print(f"❌ tkinter test failed: {e}")
        return False

def show_setup_menu():
    """Show setup and configuration menu"""
    try:
        print("Creating tkinter window...")
        root = tk.Tk()
        root.title("Customer Database Setup")
        root.geometry("500x400")
        
        # Main frame
        main_frame = tk.Frame(root, padx=20, pady=20)
        main_frame.pack(fill='both', expand=True)
        
        # Title
        title_label = tk.Label(main_frame, text="Customer Database Management System", 
                              font=('Arial', 14, 'bold'))
        title_label.pack(pady=10)
        
        subtitle_label = tk.Label(main_frame, text="Setup & Launch Menu", 
                                 font=('Arial', 12))
        subtitle_label.pack(pady=5)
        
        # Buttons frame
        buttons_frame = tk.Frame(main_frame)
        buttons_frame.pack(expand=True, fill='both', pady=20)
        
        # Menu buttons
        button_config = {'width': 30, 'pady': 5}
        
        tk.Button(buttons_frame, text="1. Check System Requirements", 
                 command=lambda: check_requirements_gui(root), **button_config).pack(pady=2)
        
        tk.Button(buttons_frame, text="2. Initialize Database (First Time)", 
                 command=lambda: init_database_gui(root), **button_config).pack(pady=2)
        
        tk.Button(buttons_frame, text="3. Launch GUI Application", 
                 command=lambda: launch_gui_app(root), **button_config).pack(pady=2)
        
        tk.Button(buttons_frame, text="4. Launch GUI (Direct)", 
                 command=lambda: launch_direct(root), **button_config).pack(pady=2)
        
        tk.Button(buttons_frame, text="5. Check Docker PostgreSQL", 
                 command=lambda: check_docker_gui(root), **button_config).pack(pady=2)
        
        tk.Button(buttons_frame, text="6. Exit", 
                 command=root.quit, **button_config).pack(pady=2)
        
        # Status label
        status_label = tk.Label(main_frame, text="Ready", fg="green")
        status_label.pack(pady=10)
        
        print("✅ tkinter window created successfully")
        root.mainloop()
        
    except Exception as e:
        print(f"❌ Error creating tkinter window: {e}")
        print("Traceback:")
        traceback.print_exc()
        return False

def check_requirements_gui(parent):
    """Check requirements and show in GUI"""
    try:
        missing_deps = check_dependencies()
        missing_files = check_database_files()
        
        if not missing_deps and not missing_files:
            messagebox.showinfo("Requirements Check", "✅ All requirements satisfied!\n\nYou can now launch the application.")
        else:
            msg = "❌ Missing Requirements:\n\n"
            if missing_deps:
                msg += "Python packages:\n"
                for pkg in missing_deps:
                    if pkg == 'psycopg2':
                        msg += f"  - {pkg} (install with: pip install psycopg2-binary)\n"
                    else:
                        msg += f"  - {pkg}\n"
                msg += "\n"
            if missing_files:
                msg += "Required files:\n"
                for file, desc in missing_files:
                    msg += f"  - {file}\n"
            messagebox.showerror("Missing Requirements", msg)
    except Exception as e:
        messagebox.showerror("Error", f"Error checking requirements: {e}")

def init_database_gui(parent):
    """Initialize database with GUI feedback"""
    try:
        missing_deps = check_dependencies()
        if 'psycopg2' in missing_deps:
            messagebox.showerror("Error", "psycopg2 is required for database operations.\n\nInstall with: pip install psycopg2-binary")
            return
        
        if not os.path.exists('db_utils.py'):
            messagebox.showerror("Error", "db_utils.py file not found!\n\nThis file is required for database initialization.")
            return
        
        # Ask for confirmation
        if messagebox.askyesno("Initialize Database", 
                              "This will create tables and sample data.\n\nProceed?"):
            messagebox.showinfo("Database Init", 
                               "Database initialization will start in the console.\n\nCheck the console window for progress.")
            try:
                import db_utils
                # Run in a separate thread to avoid blocking GUI
                import threading
                def run_init():
                    try:
                        db_utils.main()
                        messagebox.showinfo("Success", "Database initialization completed!")
                    except Exception as e:
                        messagebox.showerror("Error", f"Database initialization failed: {e}")
                
                thread = threading.Thread(target=run_init)
                thread.daemon = True
                thread.start()
                
            except ImportError as e:
                messagebox.showerror("Error", f"Could not import db_utils: {e}")
    except Exception as e:
        messagebox.showerror("Error", f"Error during database initialization: {e}")

def launch_gui_app(parent):
    """Launch the main GUI application"""
    try:
        missing_deps = check_dependencies()
        if missing_deps:
            messagebox.showerror("Error", f"Missing dependencies: {', '.join(missing_deps)}\n\nPlease install them first.")
            return
        
        if not os.path.exists('customer_db_gui.py'):
            messagebox.showerror("Error", "customer_db_gui.py file not found!\n\nThis file is required to run the application.")
            return
        
        # Close current window
        parent.quit()
        parent.destroy()
        
        # Import and run the main GUI
        try:
            import customer_db_gui
            app_root = tk.Tk()
            app = customer_db_gui.CustomerDatabaseGUI(app_root)
            app_root.mainloop()
        except ImportError as e:
            # If import fails, try running as subprocess
            messagebox.showerror("Error", f"Could not import GUI application: {e}\n\nTrying to run as separate process...")
            subprocess.run([sys.executable, 'customer_db_gui.py'])
            
    except Exception as e:
        messagebox.showerror("Error", f"Error launching GUI application: {e}")

def launch_direct(parent):
    """Launch GUI directly using subprocess"""
    try:
        if not os.path.exists('customer_db_gui.py'):
            messagebox.showerror("Error", "customer_db_gui.py file not found!")
            return
        
        messagebox.showinfo("Launching", "Starting GUI application in new window...")
        
        # Close current window
        parent.quit()
        parent.destroy()
        
        # Run GUI as subprocess
        subprocess.run([sys.executable, 'customer_db_gui.py'])
        
    except Exception as e:
        messagebox.showerror("Error", f"Error launching GUI: {e}")

def check_docker_gui(parent):
    """Check Docker PostgreSQL status"""
    try:
        result = subprocess.run(['docker', 'ps'], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            if 'postgres' in result.stdout:
                messagebox.showinfo("Docker Status", "✅ PostgreSQL container is running")
            else:
                msg = "❌ PostgreSQL container is not running\n\nWould you like to try starting it?"
                if messagebox.askyesno("Docker Status", msg):
                    try:
                        start_result = subprocess.run(['docker', 'start', 'postgres'], 
                                                    capture_output=True, text=True, timeout=30)
                        if start_result.returncode == 0:
                            messagebox.showinfo("Success", "✅ PostgreSQL container started!")
                        else:
                            messagebox.showerror("Error", f"Failed to start container:\n{start_result.stderr}")
                    except subprocess.TimeoutExpired:
                        messagebox.showerror("Error", "Docker command timed out")
                    except Exception as e:
                        messagebox.showerror("Error", f"Error starting container: {e}")
        else:
            messagebox.showerror("Docker Error", f"Docker command failed:\n{result.stderr}")
            
    except subprocess.TimeoutExpired:
        messagebox.showerror("Error", "Docker command timed out")
    except FileNotFoundError:
        messagebox.showerror("Docker Not Found", "Docker is not installed or not in PATH")
    except Exception as e:
        messagebox.showerror("Error", f"Error checking Docker: {e}")

def console_fallback():
    """Fallback console menu if tkinter fails"""
    print("\n" + "=" * 60)
    print("TKINTER GUI FAILED - USING CONSOLE MODE")
    print("=" * 60)
    
    while True:
        print("\nCustomer Database Management System - Console Menu")
        print("-" * 50)
        print("1. Check System Requirements")
        print("2. Launch GUI Application (Direct)")
        print("3. Check Files")
        print("4. Test tkinter")
        print("5. Exit")
        print("-" * 50)
        
        choice = input("Enter your choice (1-5): ").strip()
        
        if choice == '5':
            break
        elif choice == '1':
            print("\n--- System Requirements Check ---")
            missing = check_dependencies()
            missing_files = check_database_files()
            if not missing and not missing_files:
                print("✅ All requirements satisfied!")
            else:
                print("❌ Some requirements missing (see above)")
        elif choice == '2':
            if os.path.exists('customer_db_gui.py'):
                print("Launching GUI application...")
                try:
                    subprocess.run([sys.executable, 'customer_db_gui.py'])
                except Exception as e:
                    print(f"Error launching GUI: {e}")
            else:
                print("❌ customer_db_gui.py not found!")
        elif choice == '3':
            print("\n--- File Check ---")
            check_database_files()
        elif choice == '4':
            test_tkinter()
        else:
            print("Invalid choice. Please try again.")

def main():
    """Main launcher function with comprehensive error handling"""
    print("Customer Database Management System - Launcher")
    print("=" * 60)
    
    # Initial diagnostics
    print("Running initial diagnostics...")
    
    # Check Python version
    print(f"Python version: {sys.version}")
    
    # Check current directory
    print(f"Current directory: {os.getcwd()}")
    print(f"Files in directory: {os.listdir('.')}")
    
    # Test if we can import tkinter
    print("\nTesting tkinter availability...")
    if not test_tkinter():
        print("❌ tkinter is not working properly")
        print("Falling back to console mode...")
        console_fallback()
        return
    
    # Check dependencies
    print("\nChecking dependencies...")
    missing_deps = check_dependencies()
    
    # Check files
    print("\nChecking required files...")
    missing_files = check_database_files()
    
    # Try to show GUI menu
    print("\nAttempting to show GUI menu...")
    try:
        show_setup_menu()
    except Exception as e:
        print(f"❌ GUI menu failed: {e}")
        print("Traceback:")
        traceback.print_exc()
        print("\nFalling back to console mode...")
        console_fallback()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProgram interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        print("Traceback:")
        traceback.print_exc()
        print("\nTrying console fallback...")
        console_fallback()