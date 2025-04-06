import os
import sys
import subprocess
import sqlite3
import time

def create_database():
    """Create the initial database with all tables"""
    print("\n=== CREATING DATABASE ===")
    
    # SQL for creating tables
    sql_script = """
    CREATE TABLE Customer (
        CustomerID INT PRIMARY KEY,
        Customer_First_Name VARCHAR(50),
        Customer_Last_Name VARCHAR(50),
        ssn VARCHAR(20) UNIQUE,
        date_of_birth DATE,
        customer_since DATE
    );
    CREATE TABLE Address (
        addressID INT PRIMARY KEY,
        customer_id INT,
        street_address VARCHAR(255),
        city_name VARCHAR(50),
        state VARCHAR(50),
        zip_code VARCHAR(20),
        country VARCHAR(50),
        address_type VARCHAR(50),
        is_primary BOOLEAN,
        FOREIGN KEY (customer_id) REFERENCES Customer(CustomerID) ON DELETE CASCADE
    );
    CREATE TABLE Contact (
        contactID INT PRIMARY KEY,
        customer_id INT,
        contact_type VARCHAR(50),
        contact_value VARCHAR(100),
        is_primary BOOLEAN,
        FOREIGN KEY (customer_id) REFERENCES Customer(CustomerID) ON DELETE CASCADE
    );
    CREATE TABLE CustomerDocument (
        document_id INT PRIMARY KEY,
        customer_id INT,
        document_type VARCHAR(50),
        document_number VARCHAR(50) UNIQUE,
        issue_date DATE,
        expiry_date DATE,
        verification_status BOOLEAN,
        file_reference VARCHAR(255),
        FOREIGN KEY (customer_id) REFERENCES Customer(CustomerID) ON DELETE CASCADE
    );
    CREATE TABLE CustomerNote (
        note_id INT PRIMARY KEY,
        customer_id INT,
        employee_id INT,
        note_date DATE,
        note_category VARCHAR(50),
        note_text TEXT,
        is_important BOOLEAN,
        FOREIGN KEY (customer_id) REFERENCES Customer(CustomerID) ON DELETE CASCADE
    );
    CREATE TABLE CustomerSegment (
        segment_id INT PRIMARY KEY,
        segment_name VARCHAR(100),
        description TEXT,
        min_balance_required DECIMAL(10,2)
    );
    CREATE TABLE CustomerSegmentAssignment (
        assignment_id INT PRIMARY KEY,
        customer_id INT,
        segment_id INT,
        assigned_date DATE,
        FOREIGN KEY (customer_id) REFERENCES Customer(CustomerID) ON DELETE CASCADE,
        FOREIGN KEY (segment_id) REFERENCES CustomerSegment(segment_id) ON DELETE CASCADE
    );
    """
    
    # If database exists, remove it
    if os.path.exists('customer_database.db'):
        os.remove('customer_database.db')
    
    # Create database and tables
    conn = sqlite3.connect('customer_database.db')
    conn.executescript(sql_script)
    conn.commit()
    conn.close()
    
    print("Database created successfully with all required tables.")

def run_python_script(script_name):
    """Run a Python script and capture its output"""
    print(f"\n=== RUNNING {script_name} ===")
    try:
        result = subprocess.run([sys.executable, script_name], 
                               capture_output=True, text=True, check=True)
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running {script_name}:")
        print(e.stderr)
        return False

def populate_database():
    """Populate the database using different methods"""
    methods = [
        {
            "name": "Python Direct Insertion",
            "script": "data_population_script.py",
            "description": "Using Python to directly insert data into SQLite database"
        },
        {
            "name": "Excel Data Import",
            "script": "excel_import_script.py",
            "description": "Importing data from Excel files"
        },
        {
            "name": "Mockaroo API",
            "script": "mockaroo_script.py",
            "description": "Generating data using Mockaroo API"
        },
        {
            "name": "Generate Data API",
            "script": "generatedata_script.py",
            "description": "Generating data using generatedata.com API"
        }
    ]
    
    successful_methods = []
    
    for method in methods:
        print(f"\n=== METHOD: {method['name']} ===")
        print(method['description'])
        
        # Check if script exists
        if not os.path.exists(method['script']):
            print(f"Script {method['script']} not found. Skipping this method.")
            continue
        
        # Run the script
        if run_python_script(method['script']):
            successful_methods.append(method['name'])
        
        # Wait a bit between methods to avoid conflicts
        time.sleep(1)
    
    return successful_methods

def validate_database():
    """Validate the database to ensure it has enough records"""
    print("\n=== VALIDATING DATABASE ===")
    return run_python_script("validation_script.py")

def main():
    print("======================================================")
    print("      CUSTOMER DATABASE POPULATION WORKFLOW")
    print("======================================================")
    
    # Step 1: Create database
    create_database()
    
    # Step 2: Populate database using different methods
    successful_methods = populate_database()
    
    # Step 3: Validate database
    validation_success = validate_database()
    
    # Summary
    print("\n======================================================")
    print("                  WORKFLOW SUMMARY")
    print("======================================================")
    print(f"Database creation: {'Successful' if os.path.exists('customer_database.db') else 'Failed'}")
    print("Successful data population methods:")
    for method in successful_methods:
        print(f"  - {method}")
    print(f"Database validation: {'Successful' if validation_success else 'Failed'}")
    print("\nWorkflow completed.")

if __name__ == "__main__":
    main()