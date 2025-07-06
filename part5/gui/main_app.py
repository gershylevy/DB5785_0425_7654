# gui/main_app.py - Main Application Class
"""
Main application GUI class and screen management
"""
import tkinter as tk
from tkinter import ttk, messagebox
import psycopg2
from psycopg2.extras import DictCursor

from gui.screens.login_screen import LoginScreen
from gui.screens.main_menu import MainMenuScreen
from gui.screens.customer_management import CustomerManagementScreen
from gui.screens.address_management import AddressManagementScreen
from gui.screens.segment_management import SegmentManagementScreen
from gui.screens.reports_screen import ReportsScreen
from gui.screens.database_operations import DatabaseOperationsScreen

class CustomerDatabaseGUI:
    """Main application class"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Customer Database Management System")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f0f0')
        
        # Database connection variables
        self.connection = None
        self.cursor = None
        
        # Style configuration
        self.setup_styles()
        
        # Current screen
        self.current_screen = None
        
        # Start with login screen
        self.show_login_screen()
    
    def setup_styles(self):
        """Configure modern styling"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors and fonts
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'), background='#f0f0f0')
        style.configure('Heading.TLabel', font=('Arial', 12, 'bold'), background='#f0f0f0')
        style.configure('Custom.TButton', font=('Arial', 10))
        style.map('Custom.TButton', background=[('active', '#4CAF50')])
    
    def clear_screen(self):
        """Clear all widgets from the screen"""
        for widget in self.root.winfo_children():
            widget.destroy()
        self.current_screen = None
    
    def connect_database(self, host, port, database, user, password):
        """Connect to PostgreSQL database"""
        try:
            self.connection = psycopg2.connect(
                host=host,
                port=port,
                database=database,
                user=user,
                password=password
            )
            self.cursor = self.connection.cursor(cursor_factory=DictCursor)
            
            # Test connection
            self.cursor.execute("SELECT version();")
            version = self.cursor.fetchone()[0]
            
            return True, version
            
        except Exception as e:
            return False, str(e)
    
    def disconnect_database(self):
        """Disconnect from database"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        self.connection = None
        self.cursor = None
    
    # Screen Navigation Methods
    def show_login_screen(self):
        """Show login screen"""
        self.clear_screen()
        self.current_screen = LoginScreen(self.root, self)
    
    def show_main_menu(self):
        """Show main menu screen"""
        self.clear_screen()
        self.current_screen = MainMenuScreen(self.root, self)
    
    def show_customer_management(self):
        """Show customer management screen"""
        self.clear_screen()
        self.current_screen = CustomerManagementScreen(self.root, self)
    
    def show_address_management(self):
        """Show address management screen"""
        self.clear_screen()
        self.current_screen = AddressManagementScreen(self.root, self)
    
    def show_segment_management(self):
        """Show segment management screen"""
        self.clear_screen()
        self.current_screen = SegmentManagementScreen(self.root, self)
    
    def show_reports_screen(self):
        """Show reports screen"""
        self.clear_screen()
        self.current_screen = ReportsScreen(self.root, self)
    
    def show_database_operations(self):
        """Show database operations screen"""
        self.clear_screen()
        self.current_screen = DatabaseOperationsScreen(self.root, self)
    
    def create_header(self, title):
        """Create consistent header for screens"""
        header_frame = tk.Frame(self.root, bg='#34495e', height=60)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame, text=title, 
                              font=('Arial', 16, 'bold'), fg='white', bg='#34495e')
        title_label.pack(expand=True)
        
        return header_frame
