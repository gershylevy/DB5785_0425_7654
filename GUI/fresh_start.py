# fresh_start.py
import tkinter as tk
from tkinter import messagebox, simpledialog
import psycopg2

class DatabaseApp:
    def _init_(self, root):
        print("Initializing app...")
        self.root = root
        self.root.title("Database Management")
        self.root.geometry("600x400")
        self.connection = None
        self.show_login()
        print("App initialized!")
    
    def show_login(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        tk.Label(self.root, text="Database Login", font=('Arial', 16)).pack(pady=30)
        
        form = tk.Frame(self.root)
        form.pack()
        
        tk.Label(form, text="Host:").grid(row=0, column=0, padx=5, pady=5)
        self.host = tk.Entry(form)
        self.host.insert(0, "localhost")
        self.host.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(form, text="Port:").grid(row=1, column=0, padx=5, pady=5)
        self.port = tk.Entry(form)
        self.port.insert(0, "5432")
        self.port.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(form, text="Database:").grid(row=2, column=0, padx=5, pady=5)
        self.database = tk.Entry(form)
        self.database.insert(0, "postgres")
        self.database.grid(row=2, column=1, padx=5, pady=5)
        
        tk.Label(form, text="Username:").grid(row=3, column=0, padx=5, pady=5)
        self.username = tk.Entry(form)
        self.username.insert(0, "postgres")
        self.username.grid(row=3, column=1, padx=5, pady=5)
        
        tk.Label(form, text="Password:").grid(row=4, column=0, padx=5, pady=5)
        self.password = tk.Entry(form, show='*')
        self.password.grid(row=4, column=1, padx=5, pady=5)
        
        tk.Button(self.root, text="Connect", command=self.connect, 
                 bg='blue', fg='white', font=('Arial', 12)).pack(pady=20)
    
    def connect(self):
        try:
            print("Connecting to database...")
            self.connection = psycopg2.connect(
                host=self.host.get(),
                port=self.port.get(),
                database=self.database.get(),
                user=self.username.get(),
                password=self.password.get()
            )
            self.cursor = self.connection.cursor()
            print("Connected successfully!")
            messagebox.showinfo("Success", "Connected to database!")
            self.show_menu()
        except Exception as e:
            print(f"Connection failed: {e}")
            messagebox.showerror("Error", f"Connection failed:\n{e}")
    
    def show_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        tk.Label(self.root, text="Database Operations", font=('Arial', 16)).pack(pady=20)
        
        buttons = [
            ("View Customers", self.view_customers),
            ("Add Customer", self.add_customer),
            ("View Addresses", self.view_addresses),
            ("View Documents", self.view_documents),
            ("Search Customers", self.search_customers),
            ("Disconnect", self.show_login)
        ]
        
        for text, command in buttons:
            tk.Button(self.root, text=text, command=command,
                     width=20, height=2, font=('Arial', 10)).pack(pady=5)
    
    def view_customers(self):
        try:
            self.cursor.execute("SELECT * FROM Customer LIMIT 10")
            results = self.cursor.fetchall()
            self.show_results(results, "Customers")
        except Exception as e:
            messagebox.showerror("Error", f"Query failed: {e}")
    
    def view_addresses(self):
        try:
            self.cursor.execute("SELECT * FROM Address LIMIT 10")
            results = self.cursor.fetchall()
            self.show_results(results, "Addresses")
        except Exception as e:
            messagebox.showerror("Error", f"Query failed: {e}")
    
    def view_documents(self):
        try:
            self.cursor.execute("SELECT * FROM CustomerDocument LIMIT 10")
            results = self.cursor.fetchall()
            self.show_results(results, "Documents")
        except Exception as e:
            messagebox.showerror("Error", f"Query failed: {e}")
    
    def show_results(self, results, title):
        window = tk.Toplevel(self.root)
        window.title(title)
        window.geometry("800x500")
        
        tk.Label(window, text=title, font=('Arial', 14)).pack(pady=10)
        
        text = tk.Text(window, wrap='word')
        scrollbar = tk.Scrollbar(window, command=text.yview)
        text.configure(yscrollcommand=scrollbar.set)
        
        for i, row in enumerate(results, 1):
            text.insert('end', f"{i}. {row}\n\n")
        
        text.pack(side='left', expand=True, fill='both', padx=(10,0), pady=10)
        scrollbar.pack(side='right', fill='y', pady=10)
        
        tk.Button(window, text="Close", command=window.destroy).pack(pady=10)
    
    def add_customer(self):
        window = tk.Toplevel(self.root)
        window.title("Add Customer")
        window.geometry("400x350")
        
        tk.Label(window, text="Add New Customer", font=('Arial', 14)).pack(pady=10)
        
        form = tk.Frame(window)
        form.pack(pady=20)
        
        fields = ["Customer ID", "First Name", "Last Name", "SSN", "Date of Birth (YYYY-MM-DD)", "Customer Since (YYYY-MM-DD)"]
        entries = {}
        
        for i, field in enumerate(fields):
            tk.Label(form, text=f"{field}:").grid(row=i, column=0, padx=5, pady=5, sticky='w')
            entry = tk.Entry(form, width=25)
            entry.grid(row=i, column=1, padx=5, pady=5)
            entries[field] = entry
        
        def submit():
            try:
                query = """INSERT INTO Customer (CustomerID, Customer_First_Name, Customer_Last_Name, 
                                                ssn, date_of_birth, customer_since) VALUES (%s, %s, %s, %s, %s, %s)"""
                values = [entries[field].get() for field in fields]
                self.cursor.execute(query, values)
                self.connection.commit()
                messagebox.showinfo("Success", "Customer added successfully!")
                window.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add customer: {e}")
        
        tk.Button(window, text="Add Customer", command=submit, bg='green', fg='white').pack(pady=10)
        tk.Button(window, text="Cancel", command=window.destroy).pack()
    
    def search_customers(self):
        search_term = simpledialog.askstring("Search", "Enter customer name or ID:")
        if search_term:
            try:
                query = """SELECT * FROM Customer WHERE Customer_First_Name ILIKE %s 
                          OR Customer_Last_Name ILIKE %s OR CAST(CustomerID AS TEXT) LIKE %s"""
                pattern = f'%{search_term}%'
                self.cursor.execute(query, (pattern, pattern, pattern))
                results = self.cursor.fetchall()
                
                if results:
                    self.show_results(results, f"Search Results for '{search_term}'")
                else:
                    messagebox.showinfo("No Results", "No customers found.")
            except Exception as e:
                messagebox.showerror("Error", f"Search failed: {e}")

def main():
    print("Starting application...")
    root = tk.Tk()
    app = DatabaseApp(root)
    root.mainloop()
    print("Application closed.")

if __name__ == "__main__":
    main()
