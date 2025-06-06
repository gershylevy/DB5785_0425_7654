import sqlite3
import json
import random
from datetime import datetime
from faker import Faker
import os

# Initialize Faker for generating realistic data
fake = Faker()

def create_database():
    """Create the SQLite database with all necessary tables if it doesn't exist"""
    print("\n=== CREATING/CONNECTING TO DATABASE ===")
    
    # Check if database exists
    if not os.path.exists('customer_database.db'):
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
    else:
        print("Database already exists, connecting to it.")

def create_segments():
    """Create customer segments in the database"""
    print("\n=== CREATING CUSTOMER SEGMENTS (IF NEEDED) ===")
    
    conn = sqlite3.connect('customer_database.db')
    cursor = conn.cursor()
    
    # Check if segments already exist
    cursor.execute("SELECT COUNT(*) FROM CustomerSegment")
    count = cursor.fetchone()[0]
    
    if count == 0:
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
        
        conn.commit()
        print(f"Created {len(segments)} customer segments")
    else:
        print(f"Customer segments already exist ({count} segments found)")
    
    conn.close()

def method3_json_import(start_id=1, end_id=450):
    """
    Method 3: JSON Generation and Import
    
    Parameters:
        start_id (int): Starting ID for records
        end_id (int): Ending ID for records
    """
    print(f"\n=== METHOD 3: JSON GENERATION AND IMPORT (IDs {start_id}-{end_id}) ===")
    
    # Create or connect to database
    create_database()
    
    # Create segments if needed
    create_segments()
    
    # Create directory for JSON files
    os.makedirs('json_data', exist_ok=True)
    
    # ---------------------- Customer Data ----------------------
    print("Generating customer JSON data...")
    customer_data = []
    used_ssns = set()
    
    for i in range(start_id, end_id + 1):
        while True:
            ssn = f"{random.randint(100, 999)}-{random.randint(10, 99)}-{random.randint(1000, 9999)}"
            if ssn not in used_ssns:
                used_ssns.add(ssn)
                break
        
        customer_data.append({
            "CustomerID": i,
            "Customer_First_Name": fake.first_name(),
            "Customer_Last_Name": fake.last_name(),
            "ssn": ssn,
            "date_of_birth": fake.date_of_birth(minimum_age=18, maximum_age=90).strftime('%Y-%m-%d'),
            "customer_since": fake.date_between(start_date='-10y', end_date='today').strftime('%Y-%m-%d')
        })
    
    # Save customer data to JSON
    with open('json_data/customers.json', 'w') as f:
        json.dump(customer_data, f, indent=2)
    
    # ---------------------- Address Data ----------------------
    print("Generating address JSON data...")
    address_data = []
    address_types = ["Home", "Work", "Shipping", "Billing", "Secondary"]
    countries = ["Israel", "USA", "Canada", "UK", "Australia", "Germany", "France"]
    
    address_id = start_id
    for i in range(start_id, end_id + 1):
        # Each customer gets 1-3 addresses
        num_addresses = random.randint(1, 3)
        for j in range(num_addresses):
            address_data.append({
                "addressID": address_id,
                "customer_id": i,
                "street_address": fake.street_address(),
                "city_name": fake.city(),
                "state": fake.state(),
                "zip_code": fake.zipcode(),
                "country": random.choice(countries),
                "address_type": random.choice(address_types),
                "is_primary": 1 if j == 0 else 0  # First address is primary
            })
            address_id += 1
    
    # Save address data to JSON
    with open('json_data/addresses.json', 'w') as f:
        json.dump(address_data, f, indent=2)
    
    # ---------------------- Contact Data ----------------------
    print("Generating contact JSON data...")
    contact_data = []
    contact_types = ["Email", "Phone", "Mobile", "Work Phone", "Fax", "Social Media"]
    
    contact_id = start_id
    for i in range(start_id, end_id + 1):
        # Each customer gets 1-3 contacts
        num_contacts = random.randint(1, 3)
        for j in range(num_contacts):
            contact_type = random.choice(contact_types)
            
            if contact_type == "Email":
                value = fake.email()
            elif contact_type in ["Phone", "Mobile", "Work Phone"]:
                value = fake.phone_number()
            elif contact_type == "Fax":
                value = f"+1-{random.randint(100, 999)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}"
            else:  # Social Media
                value = f"@{fake.user_name()}"
            
            contact_data.append({
                "contactID": contact_id,
                "customer_id": i,
                "contact_type": contact_type,
                "contact_value": value,
                "is_primary": 1 if j == 0 else 0  # First contact is primary
            })
            contact_id += 1
    
    # Save contact data to JSON
    with open('json_data/contacts.json', 'w') as f:
        json.dump(contact_data, f, indent=2)
    
    # ---------------------- Document Data ----------------------
    print("Generating document JSON data...")
    document_data = []
    document_types = ["Passport", "Driver License", "ID Card", "Birth Certificate", "Social Security Card", "Tax ID"]
    used_document_numbers = set()
    
    document_id = start_id
    for i in range(start_id, end_id + 1):
        # Each customer gets 1-2 documents
        num_documents = random.randint(1, 2)
        for j in range(num_documents):
            doc_type = random.choice(document_types)
            
            # Generate unique document number
            while True:
                doc_num = f"{doc_type[:2].upper()}-{random.randint(10000, 999999)}"
                if doc_num not in used_document_numbers:
                    used_document_numbers.add(doc_num)
                    break
            
            document_data.append({
                "document_id": document_id,
                "customer_id": i,
                "document_type": doc_type,
                "document_number": doc_num,
                "issue_date": fake.date_between(start_date='-10y', end_date='-1y').strftime('%Y-%m-%d'),
                "expiry_date": fake.date_between(start_date='+1y', end_date='+10y').strftime('%Y-%m-%d'),
                "verification_status": 1 if random.random() < 0.8 else 0,  # 80% are verified
                "file_reference": f"DOC_{i}_{doc_type}_{document_id}.pdf"
            })
            document_id += 1
    
    # Save document data to JSON
    with open('json_data/documents.json', 'w') as f:
        json.dump(document_data, f, indent=2)
    
    # ---------------------- Note Data ----------------------
    print("Generating note JSON data...")
    note_data = []
    note_categories = ["Inquiry", "Complaint", "Request", "Feedback", "Update", "Alert"]
    note_templates = [
        "Customer called about {topic}. Resolved issue by {resolution}.",
        "Customer visited branch to discuss {topic}. {resolution}.",
        "Customer emailed regarding {topic}. {resolution}."
    ]
    topics = ["account access", "transaction dispute", "loan application", "interest rates", "fees", "online banking"]
    resolutions = [
        "Provided information",
        "Escalated to manager",
        "Reset credentials",
        "Scheduled appointment",
        "Updated account settings"
    ]
    
    note_id = start_id
    for i in range(start_id, end_id + 1):
        # Each customer gets 1-3 notes
        num_notes = random.randint(1, 3)
        for j in range(num_notes):
            employee_id = random.randint(1, 50)
            note_date = fake.date_between(start_date='-3y', end_date='today')
            category = random.choice(note_categories)
            template = random.choice(note_templates)
            topic = random.choice(topics)
            resolution = random.choice(resolutions)
            note_text = template.format(topic=topic, resolution=resolution)
            
            note_data.append({
                "note_id": note_id,
                "customer_id": i,
                "employee_id": employee_id,
                "note_date": note_date.strftime('%Y-%m-%d'),
                "note_category": category,
                "note_text": note_text,
                "is_important": 1 if random.random() < 0.2 else 0  # 20% are important
            })
            note_id += 1
    
    # Save note data to JSON
    with open('json_data/notes.json', 'w') as f:
        json.dump(note_data, f, indent=2)
    
    # ---------------------- Segment Assignment Data ----------------------
    print("Generating segment assignment JSON data...")
    segment_assignment_data = []
    
    for i in range(start_id, end_id + 1):
        # Each customer gets 1 segment assignment
        segment_id = random.randint(1, 10)
        
        segment_assignment_data.append({
            "assignment_id": i,
            "customer_id": i,
            "segment_id": segment_id,
            "assigned_date": fake.date_between(start_date='-5y', end_date='today').strftime('%Y-%m-%d')
        })
    
    # Save segment assignment data to JSON
    with open('json_data/segment_assignments.json', 'w') as f:
        json.dump(segment_assignment_data, f, indent=2)
    
    # ---------------------- Import JSON data to database ----------------------
    print("\nImporting JSON data to database...")
    
    # Connect to database
    conn = sqlite3.connect('customer_database.db')
    cursor = conn.cursor()
    
    # Import customer data
    print("Importing customer data...")
    with open('json_data/customers.json', 'r') as f:
        customers = json.load(f)
        
    for customer in customers:
        cursor.execute('''
            INSERT INTO Customer 
            (CustomerID, Customer_First_Name, Customer_Last_Name, ssn, date_of_birth, customer_since)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            customer['CustomerID'],
            customer['Customer_First_Name'],
            customer['Customer_Last_Name'],
            customer['ssn'],
            customer['date_of_birth'],
            customer['customer_since']
        ))
    
    # Import address data
    print("Importing address data...")
    with open('json_data/addresses.json', 'r') as f:
        addresses = json.load(f)
        
    for address in addresses:
        cursor.execute('''
            INSERT INTO Address 
            (addressID, customer_id, street_address, city_name, state, zip_code, country, address_type, is_primary)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            address['addressID'],
            address['customer_id'],
            address['street_address'],
            address['city_name'],
            address['state'],
            address['zip_code'],
            address['country'],
            address['address_type'],
            address['is_primary']
        ))
    
    # Import contact data
    print("Importing contact data...")
    with open('json_data/contacts.json', 'r') as f:
        contacts = json.load(f)
        
    for contact in contacts:
        cursor.execute('''
            INSERT INTO Contact 
            (contactID, customer_id, contact_type, contact_value, is_primary)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            contact['contactID'],
            contact['customer_id'],
            contact['contact_type'],
            contact['contact_value'],
            contact['is_primary']
        ))
    
    # Import document data
    print("Importing document data...")
    with open('json_data/documents.json', 'r') as f:
        documents = json.load(f)
        
    for document in documents:
        cursor.execute('''
            INSERT INTO CustomerDocument 
            (document_id, customer_id, document_type, document_number, issue_date, expiry_date, verification_status, file_reference)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            document['document_id'],
            document['customer_id'],
            document['document_type'],
            document['document_number'],
            document['issue_date'],
            document['expiry_date'],
            document['verification_status'],
            document['file_reference']
        ))
    
    # Import note data
    print("Importing note data...")
    with open('json_data/notes.json', 'r') as f:
        notes = json.load(f)
        
    for note in notes:
        cursor.execute('''
            INSERT INTO CustomerNote 
            (note_id, customer_id, employee_id, note_date, note_category, note_text, is_important)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            note['note_id'],
            note['customer_id'],
            note['employee_id'],
            note['note_date'],
            note['note_category'],
            note['note_text'],
            note['is_important']
        ))
    
    # Import segment assignment data
    print("Importing segment assignment data...")
    with open('json_data/segment_assignments.json', 'r') as f:
        assignments = json.load(f)
        
    for assignment in assignments:
        cursor.execute('''
            INSERT INTO CustomerSegmentAssignment 
            (assignment_id, customer_id, segment_id, assigned_date)
            VALUES (?, ?, ?, ?)
        ''', (
            assignment['assignment_id'],
            assignment['customer_id'],
            assignment['segment_id'],
            assignment['assigned_date']
        ))
    
    # Verify counts
    table_counts = {}
    tables = ['Customer', 'Address', 'Contact', 'CustomerDocument', 'CustomerNote', 'CustomerSegment', 'CustomerSegmentAssignment']
    
    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        table_counts[table] = count
    
    # Commit and close
    conn.commit()
    conn.close()
    
    print("\n=== DATA GENERATION SUMMARY ===")
    for table, count in table_counts.items():
        print(f"{table}: {count} records")
    
    print(f"\nMethod 3 completed successfully - Populated data for {end_id - start_id + 1} customers")

if __name__ == "__main__":
    method3_json_import(1, 450)  # Default is to populate IDs 1-450
