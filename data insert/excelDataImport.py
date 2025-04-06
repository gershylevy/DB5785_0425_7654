import pandas as pd
import sqlite3
import os

def import_excel_to_database(excel_path, table_name, db_path):
    """
    Import data from Excel file to SQLite database
    
    Parameters:
        excel_path (str): Path to Excel file
        table_name (str): Name of table to import data into
        db_path (str): Path to SQLite database
    """
    try:
        # Read Excel file
        print(f"Reading data from {excel_path}...")
        df = pd.read_excel(excel_path)
        
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
        print(f"Error importing data from {excel_path} to {table_name}: {str(e)}")

def main():
    # Database path
    db_path = 'customer_database.db'
    
    # Excel directory
    excel_dir = 'excel_data'  # Directory where your Excel files are stored
    
    # Check if database exists
    if not os.path.exists(db_path):
        print(f"Error: Database {db_path} does not exist. Please create the database first.")
        return
    
    # Check if excel directory exists
    if not os.path.exists(excel_dir):
        print(f"Error: Directory {excel_dir} does not exist.")
        return
    
    # Map Excel files to table names
    file_table_map = {
        'customer_data.xlsx': 'Customer',
        'address_data.xlsx': 'Address',
        'contact_data.xlsx': 'Contact',
        'document_data.xlsx': 'CustomerDocument',
        'note_data.xlsx': 'CustomerNote',
        'segment_data.xlsx': 'CustomerSegment',
        'segment_assignment_data.xlsx': 'CustomerSegmentAssignment'
    }
    
    # Import each Excel file to corresponding table
    for file_name, table_name in file_table_map.items():
        file_path = os.path.join(excel_dir, file_name)
        if os.path.exists(file_path):
            import_excel_to_database(file_path, table_name, db_path)
        else:
            print(f"Warning: File {file_path} does not exist. Skipping import for {table_name}.")
    
    print("Excel data import process completed.")

if __name__ == "__main__":
    main()