# complete_customer_db_gui.py - Complete Customer Database Management System
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import psycopg2
from psycopg2.extras import DictCursor
from datetime import datetime, date
import re

class CustomerDatabaseGUI:
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
    
    def show_login_screen(self):
        """Screen 1: Login Screen"""
        self.clear_screen()
        
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
    
    def connect_database(self):
        """Connect to PostgreSQL database"""
        try:
            self.connection = psycopg2.connect(
                host=self.host_entry.get(),
                port=self.port_entry.get(),
                database=self.database_entry.get(),
                user=self.username_entry.get(),
                password=self.password_entry.get()
            )
            self.cursor = self.connection.cursor(cursor_factory=DictCursor)
            
            # Test connection
            self.cursor.execute("SELECT version();")
            version = self.cursor.fetchone()[0]
            
            messagebox.showinfo("Success", f"Connected successfully!\n\nDatabase: {version[:50]}...")
            self.show_main_menu()
            
        except Exception as e:
            messagebox.showerror("Connection Error", f"Failed to connect to database:\n\n{str(e)}")
            self.status_label.config(text="Connection failed. Please check credentials.", fg='red')
    
    def show_main_menu(self):
        """Screen 2: Main Menu Screen"""
        self.clear_screen()
        
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
            ("👥 Customer Management", self.show_customer_management, '#3498db'),
            ("🏠 Address Management", self.show_address_management, '#e67e22'),
            ("📊 Segment Management", self.show_segment_management, '#9b59b6'),
            ("📈 Reports & Queries", self.show_reports_screen, '#27ae60'),
            ("🔧 Database Operations", self.show_database_operations, '#e74c3c'),
            ("🚪 Disconnect", self.show_login_screen, '#95a5a6')
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
    
    def show_customer_management(self):
        """Screen 3: Customer Management (CRUD for Customer table)"""
        self.clear_screen()
        
        # Header
        self.create_header("Customer Management")
        
        # Main content
        content_frame = tk.Frame(self.root, bg='#ecf0f1', padx=20, pady=20)
        content_frame.pack(fill='both', expand=True)
        
        # Buttons frame
        buttons_frame = tk.Frame(content_frame, bg='#ecf0f1')
        buttons_frame.pack(fill='x', pady=(0, 20))
        
        # CRUD buttons
        tk.Button(buttons_frame, text="➕ Add Customer", command=self.add_customer,
                 bg='#27ae60', fg='white', font=('Arial', 10, 'bold')).pack(side='left', padx=5)
        tk.Button(buttons_frame, text="✏️ Edit Customer", command=self.edit_customer,
                 bg='#f39c12', fg='white', font=('Arial', 10, 'bold')).pack(side='left', padx=5)
        tk.Button(buttons_frame, text="🗑️ Delete Customer", command=self.delete_customer,
                 bg='#e74c3c', fg='white', font=('Arial', 10, 'bold')).pack(side='left', padx=5)
        tk.Button(buttons_frame, text="🔄 Refresh", command=self.refresh_customers,
                 bg='#3498db', fg='white', font=('Arial', 10, 'bold')).pack(side='left', padx=5)
        tk.Button(buttons_frame, text="🔍 Search", command=self.search_customers,
                 bg='#9b59b6', fg='white', font=('Arial', 10, 'bold')).pack(side='left', padx=5)
        tk.Button(buttons_frame, text="⬅️ Back", command=self.show_main_menu,
                 bg='#95a5a6', fg='white', font=('Arial', 10, 'bold')).pack(side='right', padx=5)
        
        # Treeview for customers
        tree_frame = tk.Frame(content_frame)
        tree_frame.pack(fill='both', expand=True)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(tree_frame, orient='vertical')
        h_scrollbar = ttk.Scrollbar(tree_frame, orient='horizontal')
        
        # Treeview
        self.customer_tree = ttk.Treeview(tree_frame, 
                                         columns=('EmployeeID', 'CustomerID', 'FirstName', 'LastName', 'SSN', 'DOB', 'CustomerSince'),
                                         show='headings',
                                         yscrollcommand=v_scrollbar.set,
                                         xscrollcommand=h_scrollbar.set)
        
        # Configure scrollbars
        v_scrollbar.config(command=self.customer_tree.yview)
        h_scrollbar.config(command=self.customer_tree.xview)
        
        # Define headings
        headings = ['Employee ID', 'Customer ID', 'First Name', 'Last Name', 'SSN', 'Date of Birth', 'Customer Since']
        for i, heading in enumerate(headings):
            self.customer_tree.heading(f'#{i+1}', text=heading)
            self.customer_tree.column(f'#{i+1}', width=120)
        
        # Pack components
        self.customer_tree.pack(side='left', fill='both', expand=True)
        v_scrollbar.pack(side='right', fill='y')
        h_scrollbar.pack(side='bottom', fill='x')
        
        # Load customer data
        self.refresh_customers()
    
    def show_address_management(self):
        """Screen 4: Address Management (CRUD for Address table)"""
        self.clear_screen()
        
        # Header
        self.create_header("Address Management")
        
        # Main content
        content_frame = tk.Frame(self.root, bg='#ecf0f1', padx=20, pady=20)
        content_frame.pack(fill='both', expand=True)
        
        # Buttons frame
        buttons_frame = tk.Frame(content_frame, bg='#ecf0f1')
        buttons_frame.pack(fill='x', pady=(0, 20))
        
        # CRUD buttons
        tk.Button(buttons_frame, text="➕ Add Address", command=self.add_address,
                 bg='#27ae60', fg='white', font=('Arial', 10, 'bold')).pack(side='left', padx=5)
        tk.Button(buttons_frame, text="✏️ Edit Address", command=self.edit_address,
                 bg='#f39c12', fg='white', font=('Arial', 10, 'bold')).pack(side='left', padx=5)
        tk.Button(buttons_frame, text="🗑️ Delete Address", command=self.delete_address,
                 bg='#e74c3c', fg='white', font=('Arial', 10, 'bold')).pack(side='left', padx=5)
        tk.Button(buttons_frame, text="🔄 Refresh", command=self.refresh_addresses,
                 bg='#3498db', fg='white', font=('Arial', 10, 'bold')).pack(side='left', padx=5)
        tk.Button(buttons_frame, text="⬅️ Back", command=self.show_main_menu,
                 bg='#95a5a6', fg='white', font=('Arial', 10, 'bold')).pack(side='right', padx=5)
        
        # Treeview for addresses
        tree_frame = tk.Frame(content_frame)
        tree_frame.pack(fill='both', expand=True)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(tree_frame, orient='vertical')
        h_scrollbar = ttk.Scrollbar(tree_frame, orient='horizontal')
        
        # Treeview
        self.address_tree = ttk.Treeview(tree_frame, 
                                        columns=('AddressID', 'CustomerID', 'CustomerName', 'Street', 'City', 'State', 'ZipCode', 'Country', 'Type', 'Primary'),
                                        show='headings',
                                        yscrollcommand=v_scrollbar.set,
                                        xscrollcommand=h_scrollbar.set)
        
        # Configure scrollbars
        v_scrollbar.config(command=self.address_tree.yview)
        h_scrollbar.config(command=self.address_tree.xview)
        
        # Define headings
        headings = ['Address ID', 'Customer ID', 'Customer Name', 'Street', 'City', 'State', 'Zip Code', 'Country', 'Type', 'Primary']
        for i, heading in enumerate(headings):
            self.address_tree.heading(f'#{i+1}', text=heading)
            self.address_tree.column(f'#{i+1}', width=100)
        
        # Pack components
        self.address_tree.pack(side='left', fill='both', expand=True)
        v_scrollbar.pack(side='right', fill='y')
        h_scrollbar.pack(side='bottom', fill='x')
        
        # Load address data
        self.refresh_addresses()
    
    def show_segment_management(self):
        """Screen 5: Segment Management (CRUD for CustomerSegmentAssignment - linking table)"""
        self.clear_screen()
        
        # Header
        self.create_header("Customer Segment Management")
        
        # Main content
        content_frame = tk.Frame(self.root, bg='#ecf0f1', padx=20, pady=20)
        content_frame.pack(fill='both', expand=True)
        
        # Buttons frame
        buttons_frame = tk.Frame(content_frame, bg='#ecf0f1')
        buttons_frame.pack(fill='x', pady=(0, 20))
        
        # CRUD buttons
        tk.Button(buttons_frame, text="➕ Assign Segment", command=self.assign_segment,
                 bg='#27ae60', fg='white', font=('Arial', 10, 'bold')).pack(side='left', padx=5)
        tk.Button(buttons_frame, text="✏️ Update Assignment", command=self.update_segment_assignment,
                 bg='#f39c12', fg='white', font=('Arial', 10, 'bold')).pack(side='left', padx=5)
        tk.Button(buttons_frame, text="🗑️ Remove Assignment", command=self.remove_segment_assignment,
                 bg='#e74c3c', fg='white', font=('Arial', 10, 'bold')).pack(side='left', padx=5)
        tk.Button(buttons_frame, text="🔄 Refresh", command=self.refresh_segment_assignments,
                 bg='#3498db', fg='white', font=('Arial', 10, 'bold')).pack(side='left', padx=5)
        tk.Button(buttons_frame, text="⬅️ Back", command=self.show_main_menu,
                 bg='#95a5a6', fg='white', font=('Arial', 10, 'bold')).pack(side='right', padx=5)
        
        # Treeview for segment assignments
        tree_frame = tk.Frame(content_frame)
        tree_frame.pack(fill='both', expand=True)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(tree_frame, orient='vertical')
        h_scrollbar = ttk.Scrollbar(tree_frame, orient='horizontal')
        
        # Treeview
        self.segment_tree = ttk.Treeview(tree_frame, 
                                        columns=('AssignmentID', 'CustomerID', 'CustomerName', 'SegmentID', 'SegmentName', 'AssignedDate', 'MinBalance'),
                                        show='headings',
                                        yscrollcommand=v_scrollbar.set,
                                        xscrollcommand=h_scrollbar.set)
        
        # Configure scrollbars
        v_scrollbar.config(command=self.segment_tree.yview)
        h_scrollbar.config(command=self.segment_tree.xview)
        
        # Define headings
        headings = ['Assignment ID', 'Customer ID', 'Customer Name', 'Segment ID', 'Segment Name', 'Assigned Date', 'Min Balance']
        for i, heading in enumerate(headings):
            self.segment_tree.heading(f'#{i+1}', text=heading)
            self.segment_tree.column(f'#{i+1}', width=120)
        
        # Pack components
        self.segment_tree.pack(side='left', fill='both', expand=True)
        v_scrollbar.pack(side='right', fill='y')
        h_scrollbar.pack(side='bottom', fill='x')
        
        # Load segment assignment data
        self.refresh_segment_assignments()
    
    def show_reports_screen(self):
        """Screen 6: Reports and Queries (From part 2)"""
        self.clear_screen()
        
        # Header
        self.create_header("Reports & Database Queries")
        
        # Main content
        content_frame = tk.Frame(self.root, bg='#ecf0f1', padx=20, pady=20)
        content_frame.pack(fill='both', expand=True)
        
        # Left panel for query buttons
        left_panel = tk.Frame(content_frame, bg='#ecf0f1', width=300)
        left_panel.pack(side='left', fill='y', padx=(0, 20))
        left_panel.pack_propagate(False)
        
        tk.Label(left_panel, text="Available Reports", font=('Arial', 14, 'bold'), 
                bg='#ecf0f1', fg='#2c3e50').pack(pady=(0, 20))
        
        # Query buttons
        queries = [
            ("📋 Customers with Valid Documents", self.query_customers_valid_docs),
            ("🏠 New Customers Primary Addresses", self.query_new_customers_addresses),
            ("⚠️ Important Customer Notes", self.query_important_notes),
            ("📞 Primary Contact Information", self.query_primary_contacts),
            ("👥 Customer Segment Age Analysis", self.query_segment_age_analysis),
            ("📅 Monthly Customer Registration", self.query_monthly_registration),
            ("📊 Database Statistics", self.show_database_stats),
            ("🔧 Database Functions", self.show_database_functions)
        ]
        
        for text, command in queries:
            btn = tk.Button(left_panel, text=text, command=command,
                           bg='#3498db', fg='white', font=('Arial', 10),
                           width=35, pady=5, cursor='hand2')
            btn.pack(pady=2, fill='x')
        
        # Back button
        tk.Button(left_panel, text="⬅️ Back to Main Menu", command=self.show_main_menu,
                 bg='#95a5a6', fg='white', font=('Arial', 10, 'bold'),
                 width=35, pady=5).pack(side='bottom', pady=10, fill='x')
        
        # Right panel for results
        right_panel = tk.Frame(content_frame, bg='white', relief='sunken', bd=2)
        right_panel.pack(side='right', fill='both', expand=True)
        
        # Results area
        results_frame = tk.Frame(right_panel)
        results_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Scrolled text for results
        self.results_text = tk.Text(results_frame, font=('Courier', 10), wrap='word')
        results_scrollbar = ttk.Scrollbar(results_frame, command=self.results_text.yview)
        self.results_text.config(yscrollcommand=results_scrollbar.set)
        
        self.results_text.pack(side='left', fill='both', expand=True)
        results_scrollbar.pack(side='right', fill='y')
        
        # Initial message
        self.results_text.insert('1.0', "Select a report from the left panel to view results...\n\n")
    
    def show_database_operations(self):
        """Additional screen for database operations"""
        self.clear_screen()
        
        # Header
        self.create_header("Database Operations")
        
        # Main content
        content_frame = tk.Frame(self.root, bg='#ecf0f1', padx=20, pady=20)
        content_frame.pack(fill='both', expand=True)
        
        # Operations buttons
        operations = [
            ("📊 Database Summary", self.show_db_summary),
            ("🔄 Refresh All Data", self.refresh_all_data),
            ("📋 Export Customer List", self.export_customers),
            ("🔍 Advanced Search", self.advanced_search),
            ("📈 Generate Report", self.generate_report),
            ("⬅️ Back to Main Menu", self.show_main_menu)
        ]
        
        for text, command in operations:
            btn = tk.Button(content_frame, text=text, command=command,
                           bg='#e74c3c', fg='white', font=('Arial', 12, 'bold'),
                           width=30, height=2, cursor='hand2')
            btn.pack(pady=10)
    
    def create_header(self, title):
        """Create consistent header for screens"""
        header_frame = tk.Frame(self.root, bg='#34495e', height=60)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame, text=title, 
                              font=('Arial', 16, 'bold'), fg='white', bg='#34495e')
        title_label.pack(expand=True)
    
    # CRUD Operations for Customer
    def refresh_customers(self):
        """Load all customers into the treeview"""
        try:
            # Clear existing data
            for item in self.customer_tree.get_children():
                self.customer_tree.delete(item)
            
            # Fetch customers
            self.cursor.execute("""
                SELECT EmployeeID, CustomerID, Customer_First_Name, Customer_Last_Name, 
                       ssn, date_of_birth, customer_since 
                FROM Customer 
                ORDER BY CustomerID
            """)
            
            customers = self.cursor.fetchall()
            
            # Insert into treeview
            for customer in customers:
                self.customer_tree.insert('', 'end', values=customer)
                
            # Update status
            messagebox.showinfo("Success", f"Loaded {len(customers)} customers")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load customers: {str(e)}")
    
    def add_customer(self):
        """Add new customer"""
        dialog = CustomerDialog(self.root, "Add Customer")
        self.root.wait_window(dialog.dialog)
        
        if dialog.result:
            try:
                # Insert new customer
                self.cursor.execute("""
                    INSERT INTO Customer (EmployeeID, CustomerID, Customer_First_Name, 
                                        Customer_Last_Name, ssn, date_of_birth, customer_since)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, dialog.result)
                
                self.connection.commit()
                messagebox.showinfo("Success", "Customer added successfully!")
                self.refresh_customers()
                
            except Exception as e:
                self.connection.rollback()
                messagebox.showerror("Error", f"Failed to add customer: {str(e)}")
    
    def edit_customer(self):
        """Edit selected customer"""
        selection = self.customer_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a customer to edit")
            return
        
        # Get selected customer data
        item = self.customer_tree.item(selection[0])
        customer_data = item['values']
        
        dialog = CustomerDialog(self.root, "Edit Customer", customer_data)
        self.root.wait_window(dialog.dialog)
        
        if dialog.result:
            try:
                # Update customer
                self.cursor.execute("""
                    UPDATE Customer 
                    SET EmployeeID = %s, Customer_First_Name = %s, Customer_Last_Name = %s,
                        ssn = %s, date_of_birth = %s, customer_since = %s
                    WHERE CustomerID = %s
                """, dialog.result[:-1] + [customer_data[1]])  # Exclude CustomerID from update, use for WHERE
                
                self.connection.commit()
                messagebox.showinfo("Success", "Customer updated successfully!")
                self.refresh_customers()
                
            except Exception as e:
                self.connection.rollback()
                messagebox.showerror("Error", f"Failed to update customer: {str(e)}")
    
    def delete_customer(self):
        """Delete selected customer"""
        selection = self.customer_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a customer to delete")
            return
        
        # Get selected customer
        item = self.customer_tree.item(selection[0])
        customer_id = item['values'][1]
        customer_name = f"{item['values'][2]} {item['values'][3]}"
        
        # Confirm deletion
        if messagebox.askyesno("Confirm Delete", 
                              f"Are you sure you want to delete customer:\n{customer_name} (ID: {customer_id})?\n\nThis will also delete all related records."):
            try:
                self.cursor.execute("DELETE FROM Customer WHERE CustomerID = %s", (customer_id,))
                self.connection.commit()
                messagebox.showinfo("Success", "Customer deleted successfully!")
                self.refresh_customers()
                
            except Exception as e:
                self.connection.rollback()
                messagebox.showerror("Error", f"Failed to delete customer: {str(e)}")
    
    def search_customers(self):
        """Search customers"""
        search_term = simpledialog.askstring("Search Customers", 
                                            "Enter customer name, ID, or SSN:")
        if search_term:
            try:
                # Clear existing data
                for item in self.customer_tree.get_children():
                    self.customer_tree.delete(item)
                
                # Search customers
                self.cursor.execute("""
                    SELECT EmployeeID, CustomerID, Customer_First_Name, Customer_Last_Name, 
                           ssn, date_of_birth, customer_since 
                    FROM Customer 
                    WHERE Customer_First_Name ILIKE %s 
                       OR Customer_Last_Name ILIKE %s 
                       OR CAST(CustomerID AS TEXT) LIKE %s
                       OR ssn LIKE %s
                    ORDER BY CustomerID
                """, (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%', f'%{search_term}%'))
                
                customers = self.cursor.fetchall()
                
                # Insert search results
                for customer in customers:
                    self.customer_tree.insert('', 'end', values=customer)
                
                messagebox.showinfo("Search Results", f"Found {len(customers)} customers matching '{search_term}'")
                
            except Exception as e:
                messagebox.showerror("Error", f"Search failed: {str(e)}")
    
    # CRUD Operations for Address
    def refresh_addresses(self):
        """Load all addresses with customer names"""
        try:
            # Clear existing data
            for item in self.address_tree.get_children():
                self.address_tree.delete(item)
            
            # Fetch addresses with customer names
            self.cursor.execute("""
                SELECT a.addressID, a.customer_id, 
                       CONCAT(c.Customer_First_Name, ' ', c.Customer_Last_Name) as customer_name,
                       a.street_address, a.city_name, a.state, a.zip_code, 
                       a.country, a.address_type, a.is_primary
                FROM Address a
                JOIN Customer c ON a.customer_id = c.CustomerID
                ORDER BY a.customer_id, a.addressID
            """)
            
            addresses = self.cursor.fetchall()
            
            # Insert into treeview
            for address in addresses:
                values = list(address)
                values[-1] = "Yes" if values[-1] else "No"  # Convert boolean to text
                self.address_tree.insert('', 'end', values=values)
                
            messagebox.showinfo("Success", f"Loaded {len(addresses)} addresses")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load addresses: {str(e)}")
    
    def add_address(self):
        """Add new address"""
        dialog = AddressDialog(self.root, "Add Address", self.cursor)
        self.root.wait_window(dialog.dialog)
        
        if dialog.result:
            try:
                # Generate new address ID
                self.cursor.execute("SELECT COALESCE(MAX(addressID), 0) + 1 FROM Address")
                new_id = self.cursor.fetchone()[0]
                
                # Insert new address
                address_data = [new_id] + dialog.result
                self.cursor.execute("""
                    INSERT INTO Address (addressID, customer_id, street_address, city_name, 
                                       state, zip_code, country, address_type, is_primary)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, address_data)
                
                self.connection.commit()
                messagebox.showinfo("Success", "Address added successfully!")
                self.refresh_addresses()
                
            except Exception as e:
                self.connection.rollback()
                messagebox.showerror("Error", f"Failed to add address: {str(e)}")
    
    def edit_address(self):
        """Edit selected address"""
        selection = self.address_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an address to edit")
            return
        
        # Get selected address data
        item = self.address_tree.item(selection[0])
        address_data = item['values']
        
        dialog = AddressDialog(self.root, "Edit Address", self.cursor, address_data)
        self.root.wait_window(dialog.dialog)
        
        if dialog.result:
            try:
                # Update address
                self.cursor.execute("""
                    UPDATE Address 
                    SET customer_id = %s, street_address = %s, city_name = %s,
                        state = %s, zip_code = %s, country = %s, address_type = %s, is_primary = %s
                    WHERE addressID = %s
                """, dialog.result + [address_data[0]])
                
                self.connection.commit()
                messagebox.showinfo("Success", "Address updated successfully!")
                self.refresh_addresses()
                
            except Exception as e:
                self.connection.rollback()
                messagebox.showerror("Error", f"Failed to update address: {str(e)}")
    
    def delete_address(self):
        """Delete selected address"""
        selection = self.address_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an address to delete")
            return
        
        # Get selected address
        item = self.address_tree.item(selection[0])
        address_id = item['values'][0]
        address_info = f"{item['values'][3]}, {item['values'][4]}"
        
        # Confirm deletion
        if messagebox.askyesno("Confirm Delete", 
                              f"Are you sure you want to delete address:\n{address_info} (ID: {address_id})?"):
            try:
                self.cursor.execute("DELETE FROM Address WHERE addressID = %s", (address_id,))
                self.connection.commit()
                messagebox.showinfo("Success", "Address deleted successfully!")
                self.refresh_addresses()
                
            except Exception as e:
                self.connection.rollback()
                messagebox.showerror("Error", f"Failed to delete address: {str(e)}")
    
    # CRUD Operations for Customer Segment Assignment
    def refresh_segment_assignments(self):
        """Load all segment assignments"""
        try:
            # Clear existing data
            for item in self.segment_tree.get_children():
                self.segment_tree.delete(item)
            
            # Fetch segment assignments with customer and segment names
            self.cursor.execute("""
                SELECT csa.assignment_id, csa.customer_id, 
                       CONCAT(c.Customer_First_Name, ' ', c.Customer_Last_Name) as customer_name,
                       csa.segment_id, cs.segment_name, csa.assigned_date, cs.min_balance_required
                FROM CustomerSegmentAssignment csa
                JOIN Customer c ON csa.customer_id = c.CustomerID
                JOIN CustomerSegment cs ON csa.segment_id = cs.segment_id
                ORDER BY csa.customer_id, csa.assigned_date DESC
            """)
            
            assignments = self.cursor.fetchall()
            
            # Insert into treeview
            for assignment in assignments:
                self.segment_tree.insert('', 'end', values=assignment)
                
            messagebox.showinfo("Success", f"Loaded {len(assignments)} segment assignments")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load segment assignments: {str(e)}")
    
    def assign_segment(self):
        """Assign customer to segment"""
        dialog = SegmentAssignmentDialog(self.root, "Assign Customer to Segment", self.cursor)
        self.root.wait_window(dialog.dialog)
        
        if dialog.result:
            try:
                # Generate new assignment ID
                self.cursor.execute("SELECT COALESCE(MAX(assignment_id), 0) + 1 FROM CustomerSegmentAssignment")
                new_id = self.cursor.fetchone()[0]
                
                # Insert new assignment
                assignment_data = [new_id] + dialog.result
                self.cursor.execute("""
                    INSERT INTO CustomerSegmentAssignment (assignment_id, customer_id, segment_id, assigned_date)
                    VALUES (%s, %s, %s, %s)
                """, assignment_data)
                
                self.connection.commit()
                messagebox.showinfo("Success", "Customer assigned to segment successfully!")
                self.refresh_segment_assignments()
                
            except Exception as e:
                self.connection.rollback()
                messagebox.showerror("Error", f"Failed to assign segment: {str(e)}")
    
    def update_segment_assignment(self):
        """Update selected segment assignment"""
        selection = self.segment_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an assignment to update")
            return
        
        # Get selected assignment data
        item = self.segment_tree.item(selection[0])
        assignment_data = item['values']
        
        dialog = SegmentAssignmentDialog(self.root, "Update Segment Assignment", self.cursor, assignment_data)
        self.root.wait_window(dialog.dialog)
        
        if dialog.result:
            try:
                # Update assignment
                self.cursor.execute("""
                    UPDATE CustomerSegmentAssignment 
                    SET customer_id = %s, segment_id = %s, assigned_date = %s
                    WHERE assignment_id = %s
                """, dialog.result + [assignment_data[0]])
                
                self.connection.commit()
                messagebox.showinfo("Success", "Segment assignment updated successfully!")
                self.refresh_segment_assignments()
                
            except Exception as e:
                self.connection.rollback()
                messagebox.showerror("Error", f"Failed to update assignment: {str(e)}")
    
    def remove_segment_assignment(self):
        """Remove selected segment assignment"""
        selection = self.segment_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an assignment to remove")
            return
        
        # Get selected assignment
        item = self.segment_tree.item(selection[0])
        assignment_id = item['values'][0]
        customer_name = item['values'][2]
        segment_name = item['values'][4]
        
        # Confirm removal
        if messagebox.askyesno("Confirm Remove", 
                              f"Remove segment assignment:\n{customer_name} from {segment_name}?"):
            try:
                self.cursor.execute("DELETE FROM CustomerSegmentAssignment WHERE assignment_id = %s", (assignment_id,))
                self.connection.commit()
                messagebox.showinfo("Success", "Segment assignment removed successfully!")
                self.refresh_segment_assignments()
                
            except Exception as e:
                self.connection.rollback()
                messagebox.showerror("Error", f"Failed to remove assignment: {str(e)}")
    
    # Query Functions (From Part 2)
    def query_customers_valid_docs(self):
        """Query 1: Customers with valid documents"""
        try:
            self.cursor.execute("""
                SELECT 
                    C.Customer_First_Name, 
                    C.Customer_Last_Name, 
                    COUNT(D.document_id) AS ValidDocuments
                FROM 
                    Customer C
                JOIN 
                    CustomerDocument D ON C.CustomerID = D.customer_id
                WHERE 
                    D.expiry_date > CURRENT_DATE
                GROUP BY 
                    C.CustomerID, C.Customer_First_Name, C.Customer_Last_Name
                ORDER BY ValidDocuments DESC
            """)
            
            results = self.cursor.fetchall()
            
            # Display results
            self.results_text.delete('1.0', 'end')
            self.results_text.insert('1.0', "CUSTOMERS WITH VALID DOCUMENTS\n")
            self.results_text.insert('end', "="*50 + "\n\n")
            
            if results:
                for row in results:
                    self.results_text.insert('end', f"Customer: {row[0]} {row[1]}\n")
                    self.results_text.insert('end', f"Valid Documents: {row[2]}\n")
                    self.results_text.insert('end', "-"*30 + "\n")
            else:
                self.results_text.insert('end', "No customers with valid documents found.\n")
                
        except Exception as e:
            messagebox.showerror("Error", f"Query failed: {str(e)}")
    
    def query_new_customers_addresses(self):
        """Query 2: Primary addresses of customers who joined this year"""
        try:
            self.cursor.execute("""
                SELECT 
                    C.Customer_First_Name, 
                    C.Customer_Last_Name,
                    A.street_address, 
                    A.city_name,
                    C.customer_since
                FROM 
                    Customer C
                JOIN 
                    Address A ON C.CustomerID = A.customer_id
                WHERE 
                    A.is_primary = TRUE
                    AND EXTRACT(YEAR FROM C.customer_since) = EXTRACT(YEAR FROM CURRENT_DATE)
                ORDER BY C.customer_since DESC
            """)
            
            results = self.cursor.fetchall()
            
            # Display results
            self.results_text.delete('1.0', 'end')
            self.results_text.insert('1.0', "NEW CUSTOMERS PRIMARY ADDRESSES (This Year)\n")
            self.results_text.insert('end', "="*50 + "\n\n")
            
            if results:
                for row in results:
                    self.results_text.insert('end', f"Customer: {row[0]} {row[1]}\n")
                    self.results_text.insert('end', f"Address: {row[2]}, {row[3]}\n")
                    self.results_text.insert('end', f"Joined: {row[4]}\n")
                    self.results_text.insert('end', "-"*30 + "\n")
            else:
                self.results_text.insert('end', "No new customers found for this year.\n")
                
        except Exception as e:
            messagebox.showerror("Error", f"Query failed: {str(e)}")
    
    def query_important_notes(self):
        """Query 3: Important customer notes"""
        try:
            self.cursor.execute("""
                SELECT 
                    C.CustomerID, 
                    C.Customer_First_Name, 
                    C.Customer_Last_Name, 
                    N.note_category,
                    N.note_text,
                    N.note_date
                FROM 
                    Customer C
                JOIN 
                    CustomerNote N ON C.CustomerID = N.customer_id
                WHERE 
                    N.is_important = TRUE
                ORDER BY N.note_date DESC
            """)
            
            results = self.cursor.fetchall()
            
            # Display results
            self.results_text.delete('1.0', 'end')
            self.results_text.insert('1.0', "IMPORTANT CUSTOMER NOTES\n")
            self.results_text.insert('end', "="*50 + "\n\n")
            
            if results:
                for row in results:
                    self.results_text.insert('end', f"Customer: {row[1]} {row[2]} (ID: {row[0]})\n")
                    self.results_text.insert('end', f"Category: {row[3]}\n")
                    self.results_text.insert('end', f"Note: {row[4]}\n")
                    self.results_text.insert('end', f"Date: {row[5]}\n")
                    self.results_text.insert('end', "-"*30 + "\n")
            else:
                self.results_text.insert('end', "No important notes found.\n")
                
        except Exception as e:
            messagebox.showerror("Error", f"Query failed: {str(e)}")
    
    def query_primary_contacts(self):
        """Query 4: Primary contact information"""
        try:
            self.cursor.execute("""
                SELECT 
                    C.Customer_First_Name, 
                    C.Customer_Last_Name,
                    CT.contact_type, 
                    CT.contact_value
                FROM 
                    Customer C
                JOIN 
                    Contact CT ON C.CustomerID = CT.customer_id
                WHERE 
                    CT.is_primary = TRUE
                ORDER BY 
                    CT.contact_type, C.Customer_Last_Name
            """)
            
            results = self.cursor.fetchall()
            
            # Display results
            self.results_text.delete('1.0', 'end')
            self.results_text.insert('1.0', "PRIMARY CONTACT INFORMATION\n")
            self.results_text.insert('end', "="*50 + "\n\n")
            
            if results:
                current_type = None
                for row in results:
                    if row[2] != current_type:
                        current_type = row[2]
                        self.results_text.insert('end', f"\n{current_type.upper()}:\n")
                        self.results_text.insert('end', "-"*20 + "\n")
                    
                    self.results_text.insert('end', f"{row[0]} {row[1]}: {row[3]}\n")
            else:
                self.results_text.insert('end', "No primary contact information found.\n")
                
        except Exception as e:
            messagebox.showerror("Error", f"Query failed: {str(e)}")
    
    def query_segment_age_analysis(self):
        """Query 6: Average age by customer segment"""
        try:
            self.cursor.execute("""
                SELECT 
                    S.segment_name, 
                    ROUND(AVG(EXTRACT(YEAR FROM AGE(C.date_of_birth))), 1) AS avg_age,
                    COUNT(*) as customer_count
                FROM 
                    CustomerSegmentAssignment A
                JOIN 
                    Customer C ON C.CustomerID = A.customer_id
                JOIN 
                    CustomerSegment S ON S.segment_id = A.segment_id
                GROUP BY 
                    S.segment_name, S.segment_id
                ORDER BY avg_age DESC
            """)
            
            results = self.cursor.fetchall()
            
            # Display results
            self.results_text.delete('1.0', 'end')
            self.results_text.insert('1.0', "CUSTOMER SEGMENT AGE ANALYSIS\n")
            self.results_text.insert('end', "="*50 + "\n\n")
            
            if results:
                for row in results:
                    self.results_text.insert('end', f"Segment: {row[0]}\n")
                    self.results_text.insert('end', f"Average Age: {row[1]} years\n")
                    self.results_text.insert('end', f"Customers: {row[2]}\n")
                    self.results_text.insert('end', "-"*30 + "\n")
            else:
                self.results_text.insert('end', "No segment data found.\n")
                
        except Exception as e:
            messagebox.showerror("Error", f"Query failed: {str(e)}")
    
    def query_monthly_registration(self):
        """Query 8: Monthly customer registration"""
        try:
            self.cursor.execute("""
                SELECT 
                    EXTRACT(MONTH FROM customer_since) AS month,
                    TO_CHAR(DATE_TRUNC('month', customer_since), 'Month YYYY') as month_name,
                    COUNT(*) AS customer_count
                FROM 
                    Customer
                GROUP BY 
                    EXTRACT(MONTH FROM customer_since), DATE_TRUNC('month', customer_since)
                ORDER BY 
                    month
            """)
            
            results = self.cursor.fetchall()
            
            # Display results
            self.results_text.delete('1.0', 'end')
            self.results_text.insert('1.0', "MONTHLY CUSTOMER REGISTRATION\n")
            self.results_text.insert('end', "="*50 + "\n\n")
            
            if results:
                total = sum(row[2] for row in results)
                for row in results:
                    self.results_text.insert('end', f"Month: {row[1].strip()}\n")
                    self.results_text.insert('end', f"New Customers: {row[2]}\n")
                    percentage = (row[2] / total) * 100
                    self.results_text.insert('end', f"Percentage: {percentage:.1f}%\n")
                    self.results_text.insert('end', "-"*30 + "\n")
                
                self.results_text.insert('end', f"\nTotal Customers: {total}\n")
            else:
                self.results_text.insert('end', "No registration data found.\n")
                
        except Exception as e:
            messagebox.showerror("Error", f"Query failed: {str(e)}")
    
    def show_database_stats(self):
        """Show database statistics"""
        try:
            tables = ['Customer', 'Address', 'Contact', 'CustomerDocument', 
                     'CustomerNote', 'CustomerSegment', 'CustomerSegmentAssignment']
            
            self.results_text.delete('1.0', 'end')
            self.results_text.insert('1.0', "DATABASE STATISTICS\n")
            self.results_text.insert('end', "="*50 + "\n\n")
            
            total_records = 0
            for table in tables:
                self.cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = self.cursor.fetchone()[0]
                total_records += count
                self.results_text.insert('end', f"{table:<25}: {count:>8} records\n")
            
            self.results_text.insert('end', f"\n{'Total Records':<25}: {total_records:>8}\n")
            
            # Additional statistics
            self.cursor.execute("SELECT COUNT(DISTINCT customer_id) FROM Address")
            customers_with_addresses = self.cursor.fetchone()[0]
            
            self.cursor.execute("SELECT COUNT(DISTINCT customer_id) FROM CustomerDocument WHERE expiry_date > CURRENT_DATE")
            customers_with_valid_docs = self.cursor.fetchone()[0]
            
            self.results_text.insert('end', f"\n{'Customers with Addresses':<25}: {customers_with_addresses:>8}\n")
            self.results_text.insert('end', f"{'Customers with Valid Docs':<25}: {customers_with_valid_docs:>8}\n")
                
        except Exception as e:
            messagebox.showerror("Error", f"Query failed: {str(e)}")
    
    def show_database_functions(self):
        """Show database functions and procedures"""
        self.results_text.delete('1.0', 'end')
        self.results_text.insert('1.0', "DATABASE FUNCTIONS & PROCEDURES\n")
        self.results_text.insert('end', "="*50 + "\n\n")
        
        functions = [
            ("Update Important Notes for Seniors", self.update_senior_notes),
            ("Mark Expired Documents", self.mark_expired_documents),
            ("Promote High-Document Customers", self.promote_customers),
            ("Clean Duplicate Contacts", self.clean_duplicate_contacts)
        ]
        
        for name, func in functions:
            self.results_text.insert('end', f"• {name}\n")
        
        self.results_text.insert('end', "\nClick the buttons below to execute functions:\n\n")
        
        # Add function buttons
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)
        
        for name, func in functions:
            btn = tk.Button(button_frame, text=name, command=func,
                           bg='#e67e22', fg='white', font=('Arial', 9))
            btn.pack(side='left', padx=5)
    
    # Database Functions (From Part 2 UPDATE/DELETE operations)
    def update_senior_notes(self):
        """Mark all notes for customers over 65 as important"""
        try:
            self.cursor.execute("""
                UPDATE CustomerNote
                SET is_important = TRUE
                WHERE customer_id IN (
                    SELECT CustomerID FROM Customer 
                    WHERE EXTRACT(YEAR FROM AGE(date_of_birth)) > 65
                )
                AND is_important = FALSE
            """)
            
            affected_rows = self.cursor.rowcount
            self.connection.commit()
            
            messagebox.showinfo("Success", f"Updated {affected_rows} notes for senior customers")
            
        except Exception as e:
            self.connection.rollback()
            messagebox.showerror("Error", f"Function failed: {str(e)}")
    
    def mark_expired_documents(self):
        """Mark expired documents as unverified"""
        try:
            self.cursor.execute("""
                UPDATE CustomerDocument
                SET verification_status = FALSE
                WHERE expiry_date < CURRENT_DATE
                AND verification_status = TRUE
            """)
            
            affected_rows = self.cursor.rowcount
            self.connection.commit()
            
            messagebox.showinfo("Success", f"Marked {affected_rows} expired documents as unverified")
            
        except Exception as e:
            self.connection.rollback()
            messagebox.showerror("Error", f"Function failed: {str(e)}")
    
    def promote_customers(self):
        """Promote customers with many valid documents to Premium segment"""
        try:
            # First, check if Premium segment exists
            self.cursor.execute("SELECT segment_id FROM CustomerSegment WHERE segment_name = 'Premium'")
            premium_segment = self.cursor.fetchone()
            
            if not premium_segment:
                messagebox.showwarning("Warning", "Premium segment not found in database")
                return
            
            premium_id = premium_segment[0]
            
            # Update segment assignments
            self.cursor.execute("""
                UPDATE CustomerSegmentAssignment
                SET segment_id = %s
                WHERE customer_id IN (
                    SELECT customer_id FROM CustomerDocument
                    WHERE expiry_date > CURRENT_DATE
                    GROUP BY customer_id
                    HAVING COUNT(document_id) > 2
                )
                AND segment_id != %s
            """, (premium_id, premium_id))
            
            affected_rows = self.cursor.rowcount
            self.connection.commit()
            
            messagebox.showinfo("Success", f"Promoted {affected_rows} customers to Premium segment")
            
        except Exception as e:
            self.connection.rollback()
            messagebox.showerror("Error", f"Function failed: {str(e)}")
    
    def clean_duplicate_contacts(self):
        """Remove duplicate non-primary contacts"""
        try:
            self.cursor.execute("""
                DELETE FROM Contact
                WHERE contactID IN (
                    SELECT c1.contactID
                    FROM Contact c1
                    JOIN Contact c2 ON c1.customer_id = c2.customer_id 
                        AND c1.contact_type = c2.contact_type
                        AND c1.contact_value = c2.contact_value
                        AND c1.contactID != c2.contactID
                    WHERE c1.is_primary = FALSE
                    AND c2.is_primary = TRUE
                )
            """)
            
            affected_rows = self.cursor.rowcount
            self.connection.commit()
            
            messagebox.showinfo("Success", f"Removed {affected_rows} duplicate contact records")
            
        except Exception as e:
            self.connection.rollback()
            messagebox.showerror("Error", f"Function failed: {str(e)}")
    
    # Additional helper functions
    def show_db_summary(self):
        """Show database summary"""
        self.show_database_stats()
    
    def refresh_all_data(self):
        """Refresh all data views"""
        messagebox.showinfo("Refresh", "All data refreshed successfully!")
    
    def export_customers(self):
        """Export customer list"""
        messagebox.showinfo("Export", "Customer export feature would be implemented here")
    
    def advanced_search(self):
        """Advanced search functionality"""
        messagebox.showinfo("Search", "Advanced search feature would be implemented here")
    
    def generate_report(self):
        """Generate comprehensive report"""
        messagebox.showinfo("Report", "Report generation feature would be implemented here")


class CustomerDialog:
    """Dialog for adding/editing customers"""
    def __init__(self, parent, title, customer_data=None):
        self.result = None
        
        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("400x500")
        self.dialog.resizable(False, False)
        self.dialog.grab_set()
        
        # Center the dialog
        self.dialog.transient(parent)
        
        # Main frame
        main_frame = tk.Frame(self.dialog, padx=20, pady=20)
        main_frame.pack(fill='both', expand=True)
        
        # Title
        tk.Label(main_frame, text=title, font=('Arial', 14, 'bold')).pack(pady=(0, 20))
        
        # Form fields
        fields = [
            ('Employee ID:', 'employee_id'),
            ('Customer ID:', 'customer_id'),
            ('First Name:', 'first_name'),
            ('Last Name:', 'last_name'),
            ('SSN:', 'ssn'),
            ('Date of Birth (YYYY-MM-DD):', 'dob'),
            ('Customer Since (YYYY-MM-DD):', 'customer_since')
        ]
        
        self.entries = {}
        
        for i, (label, field) in enumerate(fields):
            tk.Label(main_frame, text=label, font=('Arial', 10)).pack(anchor='w', pady=(10, 0))
            entry = tk.Entry(main_frame, font=('Arial', 10), width=40)
            entry.pack(fill='x', pady=(0, 5))
            self.entries[field] = entry
            
            # Fill with existing data if editing
            if customer_data and i < len(customer_data):
                entry.insert(0, str(customer_data[i]))
        
        # Buttons
        button_frame = tk.Frame(main_frame)
        button_frame.pack(pady=20)
        
        tk.Button(button_frame, text="Save", command=self.save,
                 bg='#27ae60', fg='white', font=('Arial', 10, 'bold')).pack(side='left', padx=5)
        tk.Button(button_frame, text="Cancel", command=self.cancel,
                 bg='#e74c3c', fg='white', font=('Arial', 10, 'bold')).pack(side='left', padx=5)
    
    def save(self):
        """Save customer data"""
        try:
            # Validate required fields
            required_fields = ['employee_id', 'customer_id', 'first_name', 'last_name']
            for field in required_fields:
                if not self.entries[field].get().strip():
                    messagebox.showerror("Error", f"Please fill in {field.replace('_', ' ').title()}")
                    return
            
            # Validate date formats
            try:
                if self.entries['dob'].get():
                    datetime.strptime(self.entries['dob'].get(), '%Y-%m-%d')
                if self.entries['customer_since'].get():
                    datetime.strptime(self.entries['customer_since'].get(), '%Y-%m-%d')
            except ValueError:
                messagebox.showerror("Error", "Please use YYYY-MM-DD format for dates")
                return
            
            # Collect data
            self.result = [
                int(self.entries['employee_id'].get()) if self.entries['employee_id'].get() else None,
                int(self.entries['customer_id'].get()),
                self.entries['first_name'].get(),
                self.entries['last_name'].get(),
                self.entries['ssn'].get() if self.entries['ssn'].get() else None,
                self.entries['dob'].get() if self.entries['dob'].get() else None,
                self.entries['customer_since'].get() if self.entries['customer_since'].get() else None
            ]
            
            self.dialog.destroy()
            
        except ValueError as e:
            messagebox.showerror("Error", "Please check numeric fields (Employee ID, Customer ID)")
        except Exception as e:
            messagebox.showerror("Error", f"Error saving data: {str(e)}")
    
    def cancel(self):
        """Cancel dialog"""
        self.dialog.destroy()


class AddressDialog:
    """Dialog for adding/editing addresses"""
    def __init__(self, parent, title, cursor, address_data=None):
        self.result = None
        self.cursor = cursor
        
        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("450x600")
        self.dialog.resizable(False, False)
        self.dialog.grab_set()
        
        # Center the dialog
        self.dialog.transient(parent)
        
        # Main frame
        main_frame = tk.Frame(self.dialog, padx=20, pady=20)
        main_frame.pack(fill='both', expand=True)
        
        # Title
        tk.Label(main_frame, text=title, font=('Arial', 14, 'bold')).pack(pady=(0, 20))
        
        # Customer selection
        tk.Label(main_frame, text="Customer:", font=('Arial', 10, 'bold')).pack(anchor='w', pady=(10, 0))
        self.customer_var = tk.StringVar()
        self.customer_combo = ttk.Combobox(main_frame, textvariable=self.customer_var, 
                                          font=('Arial', 10), width=50, state='readonly')
        self.customer_combo.pack(fill='x', pady=(0, 5))
        
        # Load customers
        self.load_customers()
        
        # Form fields
        fields = [
            ('Street Address:', 'street_address'),
            ('City:', 'city_name'),
            ('State:', 'state'),
            ('Zip Code:', 'zip_code'),
            ('Country:', 'country'),
            ('Address Type:', 'address_type')
        ]
        
        self.entries = {}
        
        for label, field in fields:
            tk.Label(main_frame, text=label, font=('Arial', 10)).pack(anchor='w', pady=(10, 0))
            if field == 'address_type':
                # Dropdown for address type
                self.address_type_var = tk.StringVar()
                combo = ttk.Combobox(main_frame, textvariable=self.address_type_var,
                                   values=['Home', 'Work', 'Shipping', 'Billing', 'Secondary'],
                                   font=('Arial', 10), width=47, state='readonly')
                combo.pack(fill='x', pady=(0, 5))
                self.entries[field] = combo
            else:
                entry = tk.Entry(main_frame, font=('Arial', 10), width=50)
                entry.pack(fill='x', pady=(0, 5))
                self.entries[field] = entry
        
        # Primary checkbox
        self.is_primary_var = tk.BooleanVar()
        tk.Checkbutton(main_frame, text="Primary Address", variable=self.is_primary_var,
                      font=('Arial', 10)).pack(anchor='w', pady=10)
        
        # Fill with existing data if editing
        if address_data:
            self.fill_existing_data(address_data)
        
        # Buttons
        button_frame = tk.Frame(main_frame)
        button_frame.pack(pady=20)
        
        tk.Button(button_frame, text="Save", command=self.save,
                 bg='#27ae60', fg='white', font=('Arial', 10, 'bold')).pack(side='left', padx=5)
        tk.Button(button_frame, text="Cancel", command=self.cancel,
                 bg='#e74c3c', fg='white', font=('Arial', 10, 'bold')).pack(side='left', padx=5)
    
    def load_customers(self):
        """Load customer list for selection"""
        try:
            self.cursor.execute("""
                SELECT CustomerID, CONCAT(Customer_First_Name, ' ', Customer_Last_Name)
                FROM Customer ORDER BY Customer_Last_Name, Customer_First_Name
            """)
            
            customers = self.cursor.fetchall()
            customer_list = [f"{row[0]} - {row[1]}" for row in customers]
            self.customer_combo['values'] = customer_list
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load customers: {str(e)}")
    
    def fill_existing_data(self, address_data):
        """Fill form with existing address data"""
        try:
            # Set customer
            customer_id = address_data[1]
            for i, value in enumerate(self.customer_combo['values']):
                if value.startswith(str(customer_id)):
                    self.customer_combo.current(i)
                    break
            
            # Fill other fields
            self.entries['street_address'].insert(0, address_data[3] or '')
            self.entries['city_name'].insert(0, address_data[4] or '')
            self.entries['state'].insert(0, address_data[5] or '')
            self.entries['zip_code'].insert(0, address_data[6] or '')
            self.entries['country'].insert(0, address_data[7] or '')
            
            # Set address type
            if address_data[8]:
                self.address_type_var.set(address_data[8])
            
            # Set primary checkbox
            self.is_primary_var.set(address_data[9] == "Yes")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error filling form: {str(e)}")
    
    def save(self):
        """Save address data"""
        try:
            # Validate required fields
            if not self.customer_var.get():
                messagebox.showerror("Error", "Please select a customer")
                return
            
            if not self.entries['street_address'].get().strip():
                messagebox.showerror("Error", "Please enter street address")
                return
            
            # Extract customer ID
            customer_id = int(self.customer_var.get().split(' - ')[0])
            
            # Collect data
            self.result = [
                customer_id,
                self.entries['street_address'].get(),
                self.entries['city_name'].get(),
                self.entries['state'].get(),
                self.entries['zip_code'].get(),
                self.entries['country'].get(),
                self.address_type_var.get() or 'Home',
                self.is_primary_var.get()
            ]
            
            self.dialog.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error saving address: {str(e)}")
    
    def cancel(self):
        """Cancel dialog"""
        self.dialog.destroy()


class SegmentAssignmentDialog:
    """Dialog for assigning customers to segments"""
    def __init__(self, parent, title, cursor, assignment_data=None):
        self.result = None
        self.cursor = cursor
        
        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("450x400")
        self.dialog.resizable(False, False)
        self.dialog.grab_set()
        
        # Center the dialog
        self.dialog.transient(parent)
        
        # Main frame
        main_frame = tk.Frame(self.dialog, padx=20, pady=20)
        main_frame.pack(fill='both', expand=True)
        
        # Title
        tk.Label(main_frame, text=title, font=('Arial', 14, 'bold')).pack(pady=(0, 20))
        
        # Customer selection
        tk.Label(main_frame, text="Customer:", font=('Arial', 10, 'bold')).pack(anchor='w', pady=(10, 0))
        self.customer_var = tk.StringVar()
        self.customer_combo = ttk.Combobox(main_frame, textvariable=self.customer_var, 
                                          font=('Arial', 10), width=50, state='readonly')
        self.customer_combo.pack(fill='x', pady=(0, 10))
        
        # Segment selection
        tk.Label(main_frame, text="Segment:", font=('Arial', 10, 'bold')).pack(anchor='w', pady=(10, 0))
        self.segment_var = tk.StringVar()
        self.segment_combo = ttk.Combobox(main_frame, textvariable=self.segment_var, 
                                         font=('Arial', 10), width=50, state='readonly')
        self.segment_combo.pack(fill='x', pady=(0, 10))
        
        # Assignment date
        tk.Label(main_frame, text="Assignment Date (YYYY-MM-DD):", font=('Arial', 10, 'bold')).pack(anchor='w', pady=(10, 0))
        self.date_entry = tk.Entry(main_frame, font=('Arial', 10), width=50)
        self.date_entry.pack(fill='x', pady=(0, 10))
        
        # Set default date to today
        today = datetime.now().strftime('%Y-%m-%d')
        self.date_entry.insert(0, today)
        
        # Load data
        self.load_customers()
        self.load_segments()
        
        # Fill with existing data if editing
        if assignment_data:
            self.fill_existing_data(assignment_data)
        
        # Buttons
        button_frame = tk.Frame(main_frame)
        button_frame.pack(pady=20)
        
        tk.Button(button_frame, text="Save", command=self.save,
                 bg='#27ae60', fg='white', font=('Arial', 10, 'bold')).pack(side='left', padx=5)
        tk.Button(button_frame, text="Cancel", command=self.cancel,
                 bg='#e74c3c', fg='white', font=('Arial', 10, 'bold')).pack(side='left', padx=5)
    
    def load_customers(self):
        """Load customer list for selection"""
        try:
            self.cursor.execute("""
                SELECT CustomerID, CONCAT(Customer_First_Name, ' ', Customer_Last_Name)
                FROM Customer ORDER BY Customer_Last_Name, Customer_First_Name
            """)
            
            customers = self.cursor.fetchall()
            customer_list = [f"{row[0]} - {row[1]}" for row in customers]
            self.customer_combo['values'] = customer_list
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load customers: {str(e)}")
    
    def load_segments(self):
        """Load segment list for selection"""
        try:
            self.cursor.execute("""
                SELECT segment_id, segment_name, description, min_balance_required
                FROM CustomerSegment ORDER BY segment_name
            """)
            
            segments = self.cursor.fetchall()
            segment_list = [f"{row[0]} - {row[1]} (Min: ${row[3]:,.2f})" for row in segments]
            self.segment_combo['values'] = segment_list
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load segments: {str(e)}")
    
    def fill_existing_data(self, assignment_data):
        """Fill form with existing assignment data"""
        try:
            # Set customer
            customer_id = assignment_data[1]
            for i, value in enumerate(self.customer_combo['values']):
                if value.startswith(str(customer_id)):
                    self.customer_combo.current(i)
                    break
            
            # Set segment
            segment_id = assignment_data[3]
            for i, value in enumerate(self.segment_combo['values']):
                if value.startswith(str(segment_id)):
                    self.segment_combo.current(i)
                    break
            
            # Set date
            if assignment_data[5]:
                self.date_entry.delete(0, 'end')
                self.date_entry.insert(0, str(assignment_data[5]))
            
        except Exception as e:
            messagebox.showerror("Error", f"Error filling form: {str(e)}")
    
    def save(self):
        """Save segment assignment"""
        try:
            # Validate required fields
            if not self.customer_var.get():
                messagebox.showerror("Error", "Please select a customer")
                return
            
            if not self.segment_var.get():
                messagebox.showerror("Error", "Please select a segment")
                return
            
            # Validate date format
            try:
                datetime.strptime(self.date_entry.get(), '%Y-%m-%d')
            except ValueError:
                messagebox.showerror("Error", "Please use YYYY-MM-DD format for date")
                return
            
            # Extract IDs
            customer_id = int(self.customer_var.get().split(' - ')[0])
            segment_id = int(self.segment_var.get().split(' - ')[0])
            
            # Collect data
            self.result = [
                customer_id,
                segment_id,
                self.date_entry.get()
            ]
            
            self.dialog.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error saving assignment: {str(e)}")
    
    def cancel(self):
        """Cancel dialog"""
        self.dialog.destroy()


def main():
    """Main function to run the application"""
    root = tk.Tk()
    app = CustomerDatabaseGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
