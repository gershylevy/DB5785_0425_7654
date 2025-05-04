import requests
import json
import pandas as pd
import sqlite3
import os

def generate_data_api(config, num_rows, api_key):
    """
    Generate data using generatedata.com API
    
    Parameters:
        config (dict): Configuration for data generation
        num_rows (int): Number of rows to generate
        api_key (str): API key for generatedata.com
        
    Returns:
        list: Generated data
    """
    url = "https://api.generatedata.com/v1/generate"
    
    # Set the number of rows in the config
    config["numRows"] = num_rows
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    try:
        print(f"Generating {num_rows} rows of data...")
        response = requests.post(url, headers=headers, json=config)
        
        if response.status_code == 200:
            data = response.json()
            print(f"Successfully generated {len(data)} rows of data")
            return data
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return []
            
    except Exception as e:
        print(f"Error generating data: {str(e)}")
        return []

def import_to_database(data, table_name, db_path):
    """
    Import generated data to SQLite database
    
    Parameters:
        data (list): Generated data
        table_name (str): Name of table to import data into
        db_path (str): Path to SQLite database
    """
    try:
        # Convert to DataFrame
        df = pd.DataFrame(data)
        
        # Connect to database
        conn = sqlite3.connect(db_path)
        
        # Import data
        print(f"Importing {len(df)} records into {table_name}...")
        df.to_sql(table_name, conn, if_exists='append', index=False)
        
        # Verify import
        cursor = conn.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = cursor.fetchone()[0]
        print(f"Total records in {table_name} after import: {count}")
        
        # Commit and close
        conn.commit()
        conn.close()
        print(f"Successfully imported data into {table_name}")
        
    except Exception as e:
        print(f"Error importing data to {table_name}: {str(e)}")

def main():
    # generatedata.com API key - replace with your API key
    api_key = "YOUR_GENERATEDATA_API_KEY"
    
    # Database path
    db_path = 'customer_database.db'
    
    # Check if database exists
    if not os.path.exists(db_path):
        print(f"Error: Database {db_path} does not exist. Please create the database first.")
        return
    
    # Customer data configuration
    customer_config = {
        "numRows": 0,  # Will be set in the function
        "rows": [
            {"type": "autoincrement", "title": "CustomerID", "settings": {"incrementStart": 1, "incrementValue": 1}},
            {"type": "firstName", "title": "Customer_First_Name"},
            {"type": "lastName", "title": "Customer_Last_Name"},
            {"type": "sin", "title": "ssn"},
            {"type": "date", "title": "date_of_birth", "settings": {"fromDate": "1940-01-01 00:00:00", "toDate": "2003-12-31 23:59:59", "format": "Y-m-d"}},
            {"type": "date", "title": "customer_since", "settings": {"fromDate": "2010-01-01 00:00:00", "toDate": "2023-12-31 23:59:59", "format": "Y-m-d"}}
        ],
        "export": {
            "type": "JSON"
        }
    }
    
    # Address data configuration
    address_config = {
        "numRows": 0,  # Will be set in the function
        "rows": [
            {"type": "autoincrement", "title": "addressID", "settings": {"incrementStart": 1, "incrementValue": 1}},
            {"type": "numberRange", "title": "customer_id", "settings": {"min": 1, "max": 400}},
            {"type": "street", "title": "street_address"},
            {"type": "city", "title": "city_name"},
            {"type": "region", "title": "state"},
            {"type": "postcode", "title": "zip_code"},
            {"type": "country", "title": "country"},
            {"type": "list", "title": "address_type", "settings": {"listType": "exactly", "exactList": "Home,Work,Shipping,Billing,Secondary"}},
            {"type": "boolean", "title": "is_primary", "settings": {"format": "1|0"}}
        ],
        "export": {
            "type": "JSON"
        }
    }
    
    # Contact data configuration
    contact_config = {
        "numRows": 0,  # Will be set in the function
        "rows": [
            {"type": "autoincrement", "title": "contactID", "settings": {"incrementStart": 1, "incrementValue": 1}},
            {"type": "numberRange", "title": "customer_id", "settings": {"min": 1, "max": 400}},
            {"type": "list", "title": "contact_type", "settings": {"listType": "exactly", "exactList": "Email,Phone,Mobile,Work Phone,Fax,Social Media"}},
            {"type": "combined", "title": "contact_value", "settings": {
                "columns": [
                    {"type": "email", "placeholder": "{email}"},
                    {"type": "phone", "placeholder": "{phone}"},
                    {"type": "alphanumeric", "placeholder": "@{username}"}
                ],
                "template": "{% if contact_type == 'Email' %}{email}{% elseif contact_type == 'Phone' or contact_type == 'Mobile' or contact_type == 'Work Phone' or contact_type == 'Fax' %}{phone}{% else %}@{username}{% endif %}"
            }},
            {"type": "boolean", "title": "is_primary", "settings": {"format": "1|0"}}
        ],
        "export": {
            "type": "JSON"
        }
    }
    
    # Document data configuration
    document_config = {
        "numRows": 0,  # Will be set in the function
        "rows": [
            {"type": "autoincrement", "title": "document_id", "settings": {"incrementStart": 1, "incrementValue": 1}},
            {"type": "numberRange", "title": "customer_id", "settings": {"min": 1, "max": 400}},
            {"type": "list", "title": "document_type", "settings": {"listType": "exactly", "exactList": "Passport,Driver License,ID Card,Birth Certificate,Social Security Card,Tax ID"}},
            {"type": "alphanumeric", "title": "document_number", "settings": {"format": "XX-999999"}},
            {"type": "date", "title": "issue_date", "settings": {"fromDate": "2010-01-01 00:00:00", "toDate": "2022-12-31 23:59:59", "format": "Y-m-d"}},
            {"type": "date", "title": "expiry_date", "settings": {"fromDate": "2023-01-01 00:00:00", "toDate": "2033-12-31 23:59:59", "format": "Y-m-d"}},
            {"type": "boolean", "title": "verification_status", "settings": {"format": "1|0"}},
            {"type": "computed", "title": "file_reference", "settings": {"value": "DOC_{$customer_id}_{$document_type}_{$document_id}.pdf"}}
        ],
        "export": {
            "type": "JSON"
        }
    }
    
    # Note data configuration
    note_config = {
        "numRows": 0,  # Will be set in the function
        "rows": [
            {"type": "autoincrement", "title": "note_id", "settings": {"incrementStart": 1, "incrementValue": 1}},
            {"type": "numberRange", "title": "customer_id", "settings": {"min": 1, "max": 400}},
            {"type": "numberRange", "title": "employee_id", "settings": {"min": 1, "max": 50}},
            {"type": "date", "title": "note_date", "settings": {"fromDate": "2020-01-01 00:00:00", "toDate": "2023-12-31 23:59:59", "format": "Y-m-d"}},
            {"type": "list", "title": "note_category", "settings": {"listType": "exactly", "exactList": "Inquiry,Complaint,Request,Feedback,Update,Alert"}},
            {"type": "lorem", "title": "note_text", "settings": {"numParagraphs": 1, "minWordCount": 10, "maxWordCount": 30}},
            {"type": "boolean", "title": "is_important", "settings": {"format": "1|0"}}
        ],
        "export": {
            "type": "JSON"
        }
    }
    
    # Segment Assignment data configuration
    assignment_config = {
        "numRows": 0,  # Will be set in the function
        "rows": [
            {"type": "autoincrement", "title": "assignment_id", "settings": {"incrementStart": 1, "incrementValue": 1}},
            {"type": "numberRange", "title": "customer_id", "settings": {"min": 1, "max": 400}},
            {"type": "numberRange", "title": "segment_id", "settings": {"min": 1, "max": 10}},
            {"type": "date", "title": "assigned_date", "settings": {"fromDate": "2018-01-01 00:00:00", "toDate": "2023-12-31 23:59:59", "format": "Y-m-d"}}
        ],
        "export": {
            "type": "JSON"
        }
    }
    
    # Generate and import data for each configuration
    configs = [
        {"config": customer_config, "table": "Customer", "count": 401},  # 401 to account for primary key constraints
        {"config": address_config, "table": "Address", "count": 400},
        {"config": contact_config, "table": "Contact", "count": 400},
        {"config": document_config, "table": "CustomerDocument", "count": 400},
        {"config": note_config, "table": "CustomerNote", "count": 400},
        {"config": assignment_config, "table": "CustomerSegmentAssignment", "count": 400}
    ]
    
    for config_info in configs:
        # Generate data
        data = generate_data_api(config_info["config"], config_info["count"], api_key)
        
        if data:
            # Import to database
            import_to_database(data, config_info["table"], db_path)
    
    print("Generate Data API process completed.")

if __name__ == "__main__":
    main()
