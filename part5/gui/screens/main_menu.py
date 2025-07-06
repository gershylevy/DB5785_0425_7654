# gui/screens/main_menu.py - Main Menu Screen
"""
Main menu screen implementation
"""
import tkinter as tk

class MainMenuScreen:
    """Main menu screen"""
    
    def __init__(self, root, app):
        self.root = root
        self.app = app
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the main menu UI"""
        # Header
        header_frame = tk.Frame(self.root, bg='#34495e', height=80)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame, text="Customer Database Management System", 
                              font=('Arial', 18, 'bold'), fg='white', bg='#34495e')
        title_label.pack(expand=True)
        
        # Main content
        content_frame = tk.Frame(self.root, bg='#ecf0f1', padx=50, pady=30)
        content_frame.pack(fill='both', expand=True)
        
        # Welcome message
        welcome_label = tk.Label(content_frame, text="Welcome! Choose an option below:", 
                                font=('Arial', 14), bg='#ecf0f1', fg='#2c3e50')
        welcome_label.pack(pady=(0, 30))
        
        # Menu buttons frame
        buttons_frame = tk.Frame(content_frame, bg='#ecf0f1')
        buttons_frame.pack(expand=True)
        
        # Menu options
        menu_options = [
            ("👥 Customer Management", self.app.show_customer_management, '#3498db'),
            ("🏠 Address Management", self.app.show_address_management, '#e67e22'),
            ("📊 Segment Management", self.app.show_segment_management, '#9b59b6'),
            ("📈 Reports & Queries", self.app.show_reports_screen, '#27ae60'),
            ("🔧 Database Operations", self.app.show_database_operations, '#e74c3c'),
            ("🚪 Disconnect", self.disconnect_and_return, '#95a5a6')
        ]
        
        # Create buttons in grid
        for i, (text, command, color) in enumerate(menu_options):
            row = i // 2
            col = i % 2
            
            btn = tk.Button(buttons_frame, text=text, command=command,
                           bg=color, fg='white', font=('Arial', 12, 'bold'),
                           width=25, height=3, cursor='hand2',
                           relief='raised', bd=2)
            btn.grid(row=row, column=col, padx=20, pady=15)
    
    def disconnect_and_return(self):
        """Disconnect from database and return to login"""
        self.app.disconnect_database()
        self.app.show_login_screen()
