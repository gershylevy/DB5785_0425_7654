
# gui/screens/login_screen.py - Login Screen
"""
Database login screen implementation
"""
import tkinter as tk
from tkinter import messagebox

class LoginScreen:
    """Login screen for database connection"""
    
    def __init__(self, root, app):
        self.root = root
        self.app = app
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the login screen UI"""
        # Main frame
        main_frame = tk.Frame(self.root, bg='#2c3e50', padx=50, pady=50)
        main_frame.pack(fill='both', expand=True)
        
        # Title
        title_label = tk.Label(main_frame, text="Customer Database Management System", 
                              font=('Arial', 20, 'bold'), fg='white', bg='#2c3e50')
        title_label.pack(pady=(0, 30))
        
        # Login form frame
        login_frame = tk.Frame(main_frame, bg='white', padx=30, pady=30, relief='raised', bd=2)
        login_frame.pack()
        
        tk.Label(login_frame, text="Database Connection", font=('Arial', 16, 'bold')).pack(pady=(0, 20))
        
        # Connection fields
        fields_frame = tk.Frame(login_frame, bg='white')
        fields_frame.pack()
        
        # Host
        tk.Label(fields_frame, text="Host:", font=('Arial', 10, 'bold')).grid(row=0, column=0, padx=5, pady=8, sticky='e')
        self.host_entry = tk.Entry(fields_frame, font=('Arial', 10), width=20)
        self.host_entry.insert(0, "localhost")
        self.host_entry.grid(row=0, column=1, padx=5, pady=8)
        
        # Port
        tk.Label(fields_frame, text="Port:", font=('Arial', 10, 'bold')).grid(row=1, column=0, padx=5, pady=8, sticky='e')
        self.port_entry = tk.Entry(fields_frame, font=('Arial', 10), width=20)
        self.port_entry.insert(0, "5432")
        self.port_entry.grid(row=1, column=1, padx=5, pady=8)
        
        # Database
        tk.Label(fields_frame, text="Database:", font=('Arial', 10, 'bold')).grid(row=2, column=0, padx=5, pady=8, sticky='e')
        self.database_entry = tk.Entry(fields_frame, font=('Arial', 10), width=20)
        self.database_entry.insert(0, "postgres")
        self.database_entry.grid(row=2, column=1, padx=5, pady=8)
        
        # Username
        tk.Label(fields_frame, text="Username:", font=('Arial', 10, 'bold')).grid(row=3, column=0, padx=5, pady=8, sticky='e')
        self.username_entry = tk.Entry(fields_frame, font=('Arial', 10), width=20)
        self.username_entry.insert(0, "postgres")
        self.username_entry.grid(row=3, column=1, padx=5, pady=8)
        
        # Password
        tk.Label(fields_frame, text="Password:", font=('Arial', 10, 'bold')).grid(row=4, column=0, padx=5, pady=8, sticky='e')
        self.password_entry = tk.Entry(fields_frame, font=('Arial', 10), width=20, show='*')
        self.password_entry.grid(row=4, column=1, padx=5, pady=8)
        
        # Connect button
        connect_btn = tk.Button(login_frame, text="Connect to Database", 
                               command=self.connect_database,
                               bg='#3498db', fg='white', font=('Arial', 12, 'bold'),
                               padx=20, pady=10, cursor='hand2')
        connect_btn.pack(pady=20)
        
        # Status label
        self.status_label = tk.Label(login_frame, text="Enter database credentials and click Connect", 
                                    fg='#7f8c8d', bg='white')
        self.status_label.pack()
        
        # Bind Enter key to connect
        self.password_entry.bind('<Return>', lambda event: self.connect_database())
    
    def connect_database(self):
        """Connect to PostgreSQL database"""
        try:
            success, result = self.app.connect_database(
                host=self.host_entry.get(),
                port=self.port_entry.get(),
                database=self.database_entry.get(),
                user=self.username_entry.get(),
                password=self.password_entry.get()
            )
            
            if success:
                messagebox.showinfo("Success", f"Connected successfully!\n\nDatabase: {result[:50]}...")
                self.app.show_main_menu()
            else:
                raise Exception(result)
                
        except Exception as e:
            messagebox.showerror("Connection Error", f"Failed to connect to database:\n\n{str(e)}")
            self.status_label.config(text="Connection failed. Please check credentials.", fg='red')
