import sqlite3
import pandas as pd
import random
from datetime import datetime, timedelta
import csv
import requests
import json
from faker import Faker
import os

# Initialize Faker for generating realistic data
fake = Faker()

# Connect to SQLite database (you can replace with your preferred database)
conn = sqlite3.connect('customer_database.db')
cursor = conn.cursor()

# Drop tables if they exist to avoid conflicts
tables = [
    'CustomerSegmentAssignment', 'CustomerSegment', 'CustomerNote', 
    'CustomerDocument', 'Contact', 'Address', 'Customer'
]

for table in tables[::-1]:
    cursor.execute(f"DROP TABLE IF EXISTS {table}")

# Create tables using the provided SQL statements
cursor.execute('''
CREATE TABLE Customer (
    CustomerID INT PRIMARY KEY,
    Customer_First_Name VARCHAR(50),
    Customer_Last_Name VARCHAR(50),
    ssn VARCHAR(20) UNIQUE,
    date_of_birth DATE,
    customer_since DATE
)
''')

cursor.execute('''
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
)
''')

cursor.execute('''
CREATE TABLE Contact (
    contactID INT PRIMARY KEY,
    customer_id INT,
    contact_type VARCHAR(50),
    contact_value VARCHAR(100),
    is_primary BOOLEAN,
    FOREIGN KEY (customer_id) REFERENCES Customer(CustomerID) ON DELETE CASCADE
)
''')

cursor.execute('''
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
)
''')

cursor.execute('''
CREATE TABLE CustomerNote (
    note_id INT PRIMARY KEY,
    customer_id INT,
    employee_id INT,
    note_date DATE,
    note_category VARCHAR(50),
    note_text TEXT,
    is_important BOOLEAN,
    FOREIGN KEY (customer_id) REFERENCES Customer(CustomerID) ON DELETE CASCADE
)
''')

cursor.execute('''
CREATE TABLE CustomerSegment (
    segment_id INT PRIMARY KEY,
    segment_name VARCHAR(100),
    description TEXT,
    min_balance_required DECIMAL(10,2)
)
''')

cursor.execute('''
CREATE TABLE CustomerSegmentAssignment (
    assignment_id INT PRIMARY KEY,
    customer_id INT,
    segment_id INT,
    assigned_date DATE,
    FOREIGN KEY (customer_id) REFERENCES Customer(CustomerID) ON DELETE CASCADE,
    FOREIGN KEY (segment_id) REFERENCES CustomerSegment(segment_id) ON DELETE CASCADE
)
''')

# Commit the table creation
conn.commit()

# ---------------------- METHOD 1: Direct Python Insertion ----------------------

# Generate Customer data using Faker
print("Generating customer data with Python...")
customer_data = []
used_ssns = set()

for i in range(1, 200):
    while True:
        ssn = f"{random.randint(100, 999)}-{random.randint(10, 99)}-{random.randint(1000, 9999)}"
        if ssn not in used_ssns:
            used_ssns.add(ssn)
            break
    
    dob = fake.date_of_birth(minimum_age=18, maximum_age=90)
    customer_since = fake.date_between(start_date='-10y', end_date='today')
    
    customer_data.append((
        i,
        fake.first_name(),
        fake.last_name(),
        ssn,
        dob,
        customer_since
    ))

# Insert customers using direct Python insertion
cursor.executemany('''
    INSERT INTO Customer (CustomerID, Customer_First_Name, Customer_Last_Name, ssn, date_of_birth, customer_since)
    VALUES (?, ?, ?, ?, ?, ?)
''', customer_data)

# ---------------------- METHOD 2: CSV File Import ----------------------

# Generate segment data and save to CSV
print("Generating segment data and saving to CSV...")
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

# Create a CSV file for segments
with open('segments.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['segment_id', 'segment_name', 'description', 'min_balance_required'])
    writer.writerows(segments)

# Import segments from CSV
segment_df = pd.read_csv('segments.csv')
segment_df.to_sql('CustomerSegment', conn, if_exists='append', index=False)

# ---------------------- METHOD 3: Mockaroo API Import ----------------------

# Generate addresses using Mockaroo API (commented out since requires API key)
# In a real scenario, you would use:
'''
print("Fetching address data from Mockaroo...")
api_key = "your_mockaroo_api_key"
url = f"https://api.mockaroo.com/api/generate.json?key={api_key}&count=400&schema=address"
response = requests.get(url)
address_data = json.loads(response.text)
'''

# Since we can't actually call the API in this context, we'll simulate the data:
print("Generating address data (simulating Mockaroo API)...")
address_data = []
address_types = ["Home", "Work", "Shipping", "Billing", "Secondary"]
countries = ["USA", "Canada", "Israel", "UK", "Australia", "Germany", "France"]

for i in range(1, 401):
    customer_id = random.randint(1, 199)  # Match with existing customers
    address_data.append({
        "addressID": i,
        "customer_id": customer_id,
        "street_address": fake.street_address(),
        "city_name": fake.city(),
        "state": fake.state(),
        "zip_code": fake.zipcode(),
        "country": random.choice(countries),
        "address_type": random.choice(address_types),
        "is_primary": 1 if random.random() < 0.3 else 0  # 30% are primary
    })

# Insert addresses using pandas DataFrame
address_df = pd.DataFrame(address_data)
address_df.to_sql('Address', conn, if_exists='append', index=False)

# ---------------------- METHOD 4: Programmatically Generate and Insert ----------------------

# Generate contact information
print("Generating contact information...")
contact_data = []
contact_types = ["Email", "Phone", "Mobile", "Work Phone", "Fax", "Social Media"]

for i in range(1, 401):
    customer_id = random.randint(1, 199)
    contact_type = random.choice(contact_types)
    
    if contact_type == "Email":
        value = fake.email()
    elif contact_type in ["Phone", "Mobile", "Work Phone"]:
        value = fake.phone_number()
    elif contact_type == "Fax":
        value = f"+1-{random.randint(100, 999)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}"
    else:  # Social Media
        value = f"@{fake.user_name()}"
    
    contact_data.append((
        i,
        customer_id,
        contact_type,
        value,
        1 if random.random() < 0.25 else 0  # 25% are primary
    ))

# Insert contacts
cursor.executemany('''
    INSERT INTO Contact (contactID, customer_id, contact_type, contact_value, is_primary)
    VALUES (?, ?, ?, ?, ?)
''', contact_data)

# ---------------------- METHOD 5: Generate JSON and Import ----------------------

# Generate document data and save to JSON
print("Generating document data and saving to JSON...")
document_types = ["Passport", "Driver License", "ID Card", "Birth Certificate", "Social Security Card", "Tax ID"]
document_data = []
used_document_numbers = set()

for i in range(1, 401):
    customer_id = random.randint(1, 199)
    doc_type = random.choice(document_types)
    
    # Generate unique document number
    while True:
        doc_num = f"{doc_type[:2].upper()}-{random.randint(10000, 999999)}"
        if doc_num not in used_document_numbers:
            used_document_numbers.add(doc_num)
            break
    
    issue_date = fake.date_between(start_date='-10y', end_date='-1y')
    expiry_date = fake.date_between(start_date='+1y', end_date='+10y')
    
    document_data.append({
        "document_id": i,
        "customer_id": customer_id,
        "document_type": doc_type,
        "document_number": doc_num,
        "issue_date": issue_date.strftime('%Y-%m-%d'),
        "expiry_date": expiry_date.strftime('%Y-%m-%d'),
        "verification_status": 1 if random.random() < 0.8 else 0,  # 80% are verified
        "file_reference": f"DOC_{customer_id}_{doc_type}_{i}.pdf"
    })

# Save to JSON file
with open('documents.json', 'w') as f:
    json.dump(document_data, f, indent=2)

# Import from JSON
with open('documents.json', 'r') as f:
    docs = json.load(f)
    
for doc in docs:
    cursor.execute('''
        INSERT INTO CustomerDocument 
        (document_id, customer_id, document_type, document_number, issue_date, expiry_date, verification_status, file_reference)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        doc['document_id'],
        doc['customer_id'],
        doc['document_type'],
        doc['document_number'],
        doc['issue_date'],
        doc['expiry_date'],
        doc['verification_status'],
        doc['file_reference']
    ))

# ---------------------- METHOD 6: SQL Script for Direct Insertion ----------------------

# Generate notes using SQL script
print("Generating customer notes...")
note_categories = ["Inquiry", "Complaint", "Request", "Feedback", "Update", "Alert"]
note_templates = [
    "Customer called about {topic}. Resolved issue by {resolution}.",
    "Customer visited branch to discuss {topic}. {resolution}.",
    "Customer emailed regarding {topic}. {resolution}.",
    "Follow-up needed on customer's {topic}. {resolution}.",
    "Important note about customer's {topic}. {resolution}."
]
topics = ["account access", "transaction dispute", "loan application", "interest rates", "fees", "online banking"]
resolutions = [
    "Provided information",
    "Escalated to manager",
    "Reset credentials",
    "Scheduled appointment",
    "Updated account settings",
    "Submitted request form",
    "No action needed"
]

note_sql = "INSERT INTO CustomerNote (note_id, customer_id, employee_id, note_date, note_category, note_text, is_important) VALUES "
note_values = []

for i in range(1, 401):
    customer_id = random.randint(1, 199)
    employee_id = random.randint(1, 50)
    note_date = fake.date_between(start_date='-3y', end_date='today').strftime('%Y-%m-%d')
    category = random.choice(note_categories)
    template = random.choice(note_templates)
    topic = random.choice(topics)
    resolution = random.choice(resolutions)
    note_text = template.format(topic=topic, resolution=resolution)
    is_important = 1 if random.random() < 0.2 else 0  # 20% are marked important
    
    note_values.append(f"({i}, {customer_id}, {employee_id}, '{note_date}', '{category}', '{note_text}', {is_important})")

# Execute in batches to avoid statement too long error
batch_size = 50
for i in range(0, len(note_values), batch_size):
    batch = note_values[i:i+batch_size]
    cursor.execute(note_sql + ", ".join(batch))

# ---------------------- METHOD 7: Programmatically Generate Segment Assignments ----------------------

print("Generating segment assignments...")
segment_assignments = []
used_assignments = set()  # To ensure each customer has only one assignment to any segment

for i in range(1, 401):
    customer_id = random.randint(1, 199)
    segment_id = random.randint(1, 10)
    
    # Check for duplicates
    assignment_key = (customer_id, segment_id)
    if assignment_key in used_assignments:
        continue
    used_assignments.add(assignment_key)
    
    assigned_date = fake.date_between(start_date='-5y', end_date='today')
    
    segment_assignments.append((
        i,
        customer_id,
        segment_id,
        assigned_date
    ))

# Insert segment assignments
cursor.executemany('''
    INSERT INTO CustomerSegmentAssignment (assignment_id, customer_id, segment_id, assigned_date)
    VALUES (?, ?, ?, ?)
''', segment_assignments)

# ---------------------- Additional Customers to reach 400 ----------------------

# Add remaining customers to reach 400
print("Adding remaining customers to reach 400...")
remaining_customers = []
current_max_id = 199

for i in range(current_max_id + 1, 401):
    while True:
        ssn = f"{random.randint(100, 999)}-{random.randint(10, 99)}-{random.randint(1000, 9999)}"
        if ssn not in used_ssns:
            used_ssns.add(ssn)
            break
    
    dob = fake.date_of_birth(minimum_age=18, maximum_age=90)
    customer_since = fake.date_between(start_date='-10y', end_date='today')
    
    remaining_customers.append((
        i,
        fake.first_name(),
        fake.last_name(),
        ssn,
        dob,
        customer_since
    ))

# Insert remaining customers
cursor.executemany('''
    INSERT INTO Customer (CustomerID, Customer_First_Name, Customer_Last_Name, ssn, date_of_birth, customer_since)
    VALUES (?, ?, ?, ?, ?, ?)
''', remaining_customers)

# Commit all changes and close connection
conn.commit()

# Verify record counts
print("\nVerifying record counts...")
tables = ['Customer', 'Address', 'Contact', 'CustomerDocument', 'CustomerNote', 'CustomerSegment', 'CustomerSegmentAssignment']
for table in tables:
    cursor.execute(f"SELECT COUNT(*) FROM {table}")
    count = cursor.fetchone()[0]
    print(f"{table}: {count} records")

# Close connection
conn.close()
print("\nDatabase population complete!")