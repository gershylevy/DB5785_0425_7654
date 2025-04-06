import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
from faker import Faker
import os

# Initialize Faker
fake = Faker()

# Create directory for excel templates
os.makedirs('excel_templates', exist_ok=True)

# ---------------------- Customer Template ----------------------
customer_df = pd.DataFrame(columns=[
    'CustomerID', 'Customer_First_Name', 'Customer_Last_Name', 
    'ssn', 'date_of_birth', 'customer_since'
])

# Add 10 sample rows
for i in range(1, 11):
    customer_df.loc[i-1] = [
        i,
        fake.first_name(),
        fake.last_name(),
        f"{random.randint(100, 999)}-{random.randint(10, 99)}-{random.randint(1000, 9999)}",
        fake.date_of_birth(minimum_age=18, maximum_age=90).strftime('%Y-%m-%d'),
        fake.date_between(start_date='-10y', end_date='today').strftime('%Y-%m-%d')
    ]

# Save customer template
customer_df.to_excel('excel_templates/customer_template.xlsx', index=False)

# ---------------------- Address Template ----------------------
address_df = pd.DataFrame(columns=[
    'addressID', 'customer_id', 'street_address', 'city_name', 
    'state', 'zip_code', 'country', 'address_type', 'is_primary'
])

# Add 10 sample rows
address_types = ["Home", "Work", "Shipping", "Billing", "Secondary"]
countries = ["Israel", "USA", "Canada", "UK", "Australia", "Germany", "France"]

for i in range(1, 11):
    address_df.loc[i-1] = [
        i,
        random.randint(1, 10),
        fake.street_address(),
        fake.city(),
        fake.state(),
        fake.zipcode(),
        random.choice(countries),
        random.choice(address_types),
        1 if random.random() < 0.3 else 0
    ]

# Save address template
address_df.to_excel('excel_templates/address_template.xlsx', index=False)

# ---------------------- Contact Template ----------------------
contact_df = pd.DataFrame(columns=[
    'contactID', 'customer_id', 'contact_type', 'contact_value', 'is_primary'
])

# Add 10 sample rows
contact_types = ["Email", "Phone", "Mobile", "Work Phone", "Fax", "Social Media"]

for i in range(1, 11):
    customer_id = random.randint(1, 10)
    contact_type = random.choice(contact_types)
    
    if contact_type == "Email":
        value = fake.email()
    elif contact_type in ["Phone", "Mobile", "Work Phone"]:
        value = fake.phone_number()
    elif contact_type == "Fax":
        value = f"+1-{random.randint(100, 999)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}"
    else:  # Social Media
        value = f"@{fake.user_name()}"
        
    contact_df.loc[i-1] = [
        i,
        customer_id,
        contact_type,
        value,
        1 if random.random() < 0.25 else 0
    ]

# Save contact template
contact_df.to_excel('excel_templates/contact_template.xlsx', index=False)

# ---------------------- Document Template ----------------------
document_df = pd.DataFrame(columns=[
    'document_id', 'customer_id', 'document_type', 'document_number',
    'issue_date', 'expiry_date', 'verification_status', 'file_reference'
])

# Add 10 sample rows
document_types = ["Passport", "Driver License", "ID Card", "Birth Certificate", "Social Security Card", "Tax ID"]
used_document_numbers = set()

for i in range(1, 11):
    customer_id = random.randint(1, 10)
    doc_type = random.choice(document_types)
    
    # Generate unique document number
    while True:
        doc_num = f"{doc_type[:2].upper()}-{random.randint(10000, 999999)}"
        if doc_num not in used_document_numbers:
            used_document_numbers.add(doc_num)
            break
    
    issue_date = fake.date_between(start_date='-10y', end_date='-1y').strftime('%Y-%m-%d')
    expiry_date = fake.date_between(start_date='+1y', end_date='+10y').strftime('%Y-%m-%d')
    
    document_df.loc[i-1] = [
        i,
        customer_id,
        doc_type,
        doc_num,
        issue_date,
        expiry_date,
        1 if random.random() < 0.8 else 0,
        f"DOC_{customer_id}_{doc_type}_{i}.pdf"
    ]

# Save document template
document_df.to_excel('excel_templates/document_template.xlsx', index=False)

# ---------------------- Note Template ----------------------
note_df = pd.DataFrame(columns=[
    'note_id', 'customer_id', 'employee_id', 'note_date', 
    'note_category', 'note_text', 'is_important'
])

# Add 10 sample rows
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

for i in range(1, 11):
    customer_id = random.randint(1, 10)
    employee_id = random.randint(1, 20)
    note_date = fake.date_between(start_date='-3y', end_date='today').strftime('%Y-%m-%d')
    category = random.choice(note_categories)
    template = random.choice(note_templates)
    topic = random.choice(topics)
    resolution = random.choice(resolutions)
    note_text = template.format(topic=topic, resolution=resolution)
    
    note_df.loc[i-1] = [
        i,
        customer_id,
        employee_id,
        note_date,
        category,
        note_text,
        1 if random.random() < 0.2 else 0
    ]

# Save note template
note_df.to_excel('excel_templates/note_template.xlsx', index=False)

# ---------------------- Segment Template ----------------------
segment_df = pd.DataFrame([
    [1, "Premium", "High-value customers with significant assets", 50000.00],
    [2, "Standard", "Regular customers with moderate financial activity", 5000.00],
    [3, "Basic", "Entry-level customers with minimal financial activity", 500.00],
    [4, "Student", "Young customers with educational focus", 100.00],
    [5, "Senior", "Customers over 65 with retirement needs", 1000.00],
    [6, "Business", "Small business owners and entrepreneurs", 10000.00],
    [7, "Executive", "High-ranking professionals with complex needs", 25000.00],
    [8, "International", "Customers with international banking needs", 15000.00],
    [9, "Digital", "Tech-savvy customers who prefer online banking", 250.00],
    [10, "Family", "Customers with family-focused financial planning", 2500.00]