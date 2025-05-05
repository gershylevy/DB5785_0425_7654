import sqlite3
import os
import sys

def check_prerequisites():
    """Check that all required modules are installed"""
    try:
        import pandas
        import faker
        import json
        print("All required modules are installed.")
        return True
    except ImportError as e:
        print(f"Error: Missing required module - {e}")
        print("Please install the required modules with:")
        print("pip install pandas faker")
        return False

def create_database():
    """Create the initial database with all tables"""
    print("\n=== CREATING DATABASE ===")
    
    # Remove existing database if it exists
    if os.path.exists('customer_database.db'):
        os.remove('customer_database.db')
        print("Removed existing database.")
    
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
    
    # Create database and tables
    conn = sqlite3.connect('customer_database.db')
    conn.executescript(sql_script)
    conn.commit()
    conn.close()
    
    print("Database created successfully with all required tables.")

def create_segments():
    """Create the CustomerSegment table data"""
    print("\n=== CREATING CUSTOMER SEGMENTS ===")
    
    # Connect to database
    conn = sqlite3.connect('customer_database.db')
    cursor = conn.cursor()
    
    # Define segments
    segments = [
        (1, "Premium", "High-value customers with significant assets", 50000.00),
        (2, "Standard", "Regular customers with moderate financial activity", 5000.00),
        (3, "Basic", "Entry-level customers with minimal financial activity", 500.00),
        (4, "Student", "Young customers with educational focus", 100.00),
        (5, "Senior", "Customers over 65 with retirement needs", 1000.00),
        (6, "Business", "Small business owners and entrepreneurs", 10000.00),
        (7, "Executive", "High-ranking professionals with complex needs", 25000.00),
        (8, "International", "Customers with international banking needs", 15000.00),
        (9, "Digital", "Tech-savvy customers who prefer online banking", 250.00),
        (10, "Family", "Customers with family-focused financial planning", 2500.00)
    ]
    
    # Insert segments
    cursor.executemany('''
        INSERT INTO CustomerSegment (segment_id, segment_name, description, min_balance_required)
        VALUES (?, ?, ?, ?)
    ''', segments)
    
    # Commit and close
    conn.commit()
    conn.close()
    
    print(f"Created {len(segments)} customer segments")

def validate_database(min_records=400):
    """Validate the database to ensure it has sufficient records"""
    print("\n=== VALIDATING DATABASE ===")
    
    # Connect to database
    conn = sqlite3.connect('customer_database.db')
    cursor = conn.cursor()
    
    # Check record count for each table
    tables = [
        'Customer', 
        'Address', 
        'Contact', 
        'CustomerDocument', 
        'CustomerNote', 
        'CustomerSegment', 
        'CustomerSegmentAssignment'
    ]
    
    all_valid = True
    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        if table == 'CustomerSegment':
            status = "✓ PASS" if count == 10 else "✗ FAIL"
        else:
            status = "✓ PASS" if count >= min_records else "✗ FAIL"
            
        print(f"{table}: {count} records - {status}")
        
        if status == "✗ FAIL":
            all_valid = False
    
    # Close connection
    conn.close()
    
    if all_valid:
        print("\nVALIDATION SUCCESSFUL: All tables have the required number of records")
    else:
        print("\nVALIDATION FAILED: Some tables do not have the required number of records")
    
    return all_valid

def main():
    """Main function to coordinate the population of the database"""
    print("======================================================")
    print("      CUSTOMER DATABASE POPULATION COORDINATOR")
    print("======================================================")
    
    # Check prerequisites
    if not check_prerequisites():
        return 1
    
    # Create the database structure
    create_database()
    
    # Create the segments (common for all methods)
    create_segments()
    
    # Define ID ranges for each method
    total_customers = 450  # Total number of customers to generate
    customers_per_method = total_customers // 3
    
    method1_start = 1
    method1_end = method1_start + customers_per_method - 1
    
    method2_start = method1_end + 1
    method2_end = method2_start + customers_per_method - 1
    
    method3_start = method2_end + 1
    method3_end = total_customers
    
    # Import and run method 1 (Direct Python Insertion)
    print("\n=== RUNNING METHOD 1: DIRECT PYTHON INSERTION ===")
    from method1_direct_insertion import method1_direct_insertion
    method1_direct_insertion(method1_start, method1_end)
    
    # Import and run method 2 (Excel Import)
    print("\n=== RUNNING METHOD 2: EXCEL IMPORT ===")
    from method2_excel_import import method2_excel_import
    method2_excel_import(method2_start, method2_end)
    
    # Import and run method 3 (JSON Import)
    print("\n=== RUNNING METHOD 3: JSON IMPORT ===")
    from method3_json_import import method3_json_import
    method3_json_import(method3_start, method3_end)
    
    # Validate the database
    is_valid = validate_database()
    
    print("\n======================================================")
    print("                  PROCESS SUMMARY")
    print("======================================================")
    print(f"Method 1 (Direct Python Insertion): IDs {method1_start}-{method1_end}")
    print(f"Method 2 (Excel Import): IDs {method2_start}-{method2_end}")
    print(f"Method 3 (JSON Import): IDs {method3_start}-{method3_end}")
    print("\nDatabase population completed.")
    
    return 0 if is_valid else 1

if __name__ == "__main__":
    sys.exit(main())
