import requests
import json
import pandas as pd
import os
import time

def generate_mockaroo_data(schema_name, count, api_key):
    """
    Generate data using Mockaroo API
    
    Parameters:
        schema_name (str): Name of schema to use (must be created in Mockaroo)
        count (int): Number of records to generate
        api_key (str): Mockaroo API key
        
    Returns:
        list: Generated data in JSON format
    """
    url = f"https://api.mockaroo.com/api/generate.json"
    params = {
        "key": api_key,
        "count": count,
        "schema": schema_name
    }
    
    try:
        print(f"Generating {count} records for {schema_name}...")
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            print(f"Successfully generated {len(data)} records for {schema_name}")
            return data
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return []
    
    except Exception as e:
        print(f"Error generating data for {schema_name}: {str(e)}")
        return []

def save_data_to_excel(data, file_path):
    """
    Save data to Excel file
    
    Parameters:
        data (list): Data to save
        file_path (str): Path to save Excel file
    """
    try:
        # Convert to DataFrame
        df = pd.DataFrame(data)
        
        # Save to Excel
        df.to_excel(file_path, index=False)
        print(f"Successfully saved data to {file_path}")
    
    except Exception as e:
        print(f"Error saving data to {file_path}: {str(e)}")

def main():
    # Mockaroo API key - replace with your API key
    api_key = "YOUR_MOCKAROO_API_KEY"
    
    # Create directory for Excel files
    excel_dir = 'excel_data'
    os.makedirs(excel_dir, exist_ok=True)
    
    # Define schemas and record counts
    schemas = [
        {"name": "customer", "count": 400, "file": "customer_data.xlsx"},
        {"name": "address", "count": 400, "file": "address_data.xlsx"},
        {"name": "contact", "count": 400, "file": "contact_data.xlsx"},
        {"name": "document", "count": 400, "file": "document_data.xlsx"},
        {"name": "note", "count": 400, "file": "note_data.xlsx"},
        {"name": "segment_assignment", "count": 400, "file": "segment_assignment_data.xlsx"}
    ]
    
    # Generate data for each schema
    for schema in schemas:
        # Generate data using Mockaroo API
        data = generate_mockaroo_data(schema["name"], schema["count"], api_key)
        
        if data:
            # Save to Excel
            file_path = os.path.join(excel_dir, schema["file"])
            save_data_to_excel(data, file_path)
        
        # Sleep to avoid API rate limits
        time.sleep(1)
    
    print("Mockaroo data generation process completed.")

"""
IMPORTANT: Before running this script, you need to create the following schemas in Mockaroo:

1. customer schema:
   - CustomerID: Row Number
   - Customer_First_Name: First Name
   - Customer_Last_Name: Last Name
   - ssn: SSN
   - date_of_birth: Date (yyyy-MM-dd, between 1940-01-01 and 2003-12-31)
   - customer_since: Date (yyyy-MM-dd, between 2010-01-01 and 2023-12-31)

2. address schema:
   - addressID: Row Number
   - customer_id: Number (between 1 and 400)
   - street_address: Street Address
   - city_name: City
   - state: State
   - zip_code: Postal Code
   - country: Country
   - address_type: Custom List (Home, Work, Shipping, Billing, Secondary)
   - is_primary: Boolean

3. contact schema:
   - contactID: Row Number
   - customer_id: Number (between 1 and 400)
   - contact_type: Custom List (Email, Phone, Mobile, Work Phone, Fax, Social Media)
   - contact_value: Formula (IF(contact_type="Email",email(),IF(contact_type="Phone",phone(),IF(contact_type="Mobile",mobile(),IF(contact_type="Work Phone",phone(),IF(contact_type="Fax",phone(),CONCAT("@",username())))))))
   - is_primary: Boolean

4. document schema:
   - document_id: Row Number
   - customer_id: Number (between 1 and 400)
   - document_type: Custom List (Passport, Driver License, ID Card, Birth Certificate, Social Security Card, Tax ID)
   - document_number: Regular Expression ([A-Z]{2}-[0-9]{6})
   - issue_date: Date (yyyy-MM-dd, between 2010-01-01 and 2022-12-31)
   - expiry_date: Date (yyyy-MM-dd, between 2023-01-01 and 2033-12-31)
   - verification_status: Boolean
   - file_reference: Formula (CONCAT("DOC_",customer_id,"_",document_type,"_",document_id,".pdf"))

5. note schema:
   - note_id: Row Number
   - customer_id: Number (between 1 and 400)
   - employee_id: Number (between 1 and 50)
   - note_date: Date (yyyy-MM-dd, between 2020-01-01 and 2023-12-31)
   - note_category: Custom List (Inquiry, Complaint, Request, Feedback, Update, Alert)
   - note_text: Custom List (with various customer service notes)
   - is_important: Boolean

6. segment_assignment schema:
   - assignment_id: Row Number
   - customer_id: Number (between 1 and 400)
   - segment_id: Number (between 1 and 10)
   - assigned_date: Date (yyyy-MM-dd, between 2018-01-01 and 2023-12-31)
"""

if __name__ == "__main__":
    main()