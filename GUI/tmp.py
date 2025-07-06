# diagnostic.py - Quick diagnostic script
import sys
import os
import traceback

def run_diagnostics():
    """Run comprehensive diagnostics"""
    print("=" * 60)
    print("CUSTOMER DATABASE LAUNCHER DIAGNOSTICS")
    print("=" * 60)
    
    # 1. Python Information
    print(f"\n1. PYTHON INFORMATION:")
    print(f"   Version: {sys.version}")
    print(f"   Executable: {sys.executable}")
    print(f"   Platform: {sys.platform}")
    
    # 2. Current Directory
    print(f"\n2. CURRENT DIRECTORY:")
    print(f"   Path: {os.getcwd()}")
    print(f"   Files: {', '.join(os.listdir('.'))}")
    
    # 3. Required Files Check
    print(f"\n3. REQUIRED FILES CHECK:")
    required_files = ['customer_db_gui.py', 'launcher.py']
    for file in required_files:
        if os.path.exists(file):
            size = os.path.getsize(file)
            print(f"   ✅ {file} ({size} bytes)")
        else:
            print(f"   ❌ {file} (MISSING)")
    
    # 4. Python Modules Check
    print(f"\n4. PYTHON MODULES CHECK:")
    modules = ['tkinter', 'psycopg2']
    for module in modules:
        try:
            __import__(module)
            print(f"   ✅ {module}")
        except ImportError as e:
            print(f"   ❌ {module} - {e}")
    
    # 5. Tkinter Test
    print(f"\n5. TKINTER TEST:")
    try:
        import tkinter as tk
        root = tk.Tk()
        root.withdraw()
        root.title("Test Window")
        root.geometry("100x100")
        root.after(100, root.destroy)  # Auto-close after 100ms
        root.mainloop()
        print("   ✅ tkinter working correctly")
    except Exception as e:
        print(f"   ❌ tkinter error: {e}")
        traceback.print_exc()
    
    # 6. Import Test
    print(f"\n6. IMPORT TEST:")
    try:
        # Test importing the main GUI module
        if os.path.exists('customer_db_gui.py'):
            # Add current directory to path
            sys.path.insert(0, os.getcwd())
            import customer_db_gui
            print("   ✅ customer_db_gui.py imports successfully")
        else:
            print("   ❌ customer_db_gui.py not found")
    except Exception as e:
        print(f"   ❌ Import error: {e}")
        traceback.print_exc()
    
    # 7. Launcher Test
    print(f"\n7. LAUNCHER SCRIPT TEST:")
    try:
        if os.path.exists('launcher.py'):
            # Try to read the launcher file
            with open('launcher.py', 'r') as f:
                content = f.read()
                lines = len(content.split('\n'))
                print(f"   ✅ launcher.py readable ({lines} lines)")
                
                # Check for syntax errors
                compile(content, 'launcher.py', 'exec')
                print("   ✅ launcher.py syntax OK")
        else:
            print("   ❌ launcher.py not found")
    except Exception as e:
        print(f"   ❌ Launcher error: {e}")
    
    # 8. Recommendations
    print(f"\n8. RECOMMENDATIONS:")
    
    # Check if customer_db_gui.py works
    if os.path.exists('customer_db_gui.py'):
        print("   ➤ Try running: python customer_db_gui.py")
    
    # Check tkinter issues
    try:
        import tkinter
        print("   ➤ tkinter is available")
    except ImportError:
        if sys.platform.startswith('linux'):
            print("   ➤ Install tkinter: sudo apt-get install python3-tk")
        elif sys.platform == 'darwin':
            print("   ➤ Install tkinter: brew install python-tk")
        else:
            print("   ➤ Reinstall Python with tkinter support")
    
    # Check psycopg2
    try:
        import psycopg2
    except ImportError:
        print("   ➤ Install psycopg2: pip install psycopg2-binary")
    
    print(f"\n9. NEXT STEPS:")
    print("   1. If customer_db_gui.py works, use that directly")
    print("   2. If launcher fails, use the fixed launcher: python launcher_fixed.py")
    print("   3. Check error messages above for specific issues")
    print("   4. Ensure all required files are in the same directory")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    run_diagnostics()