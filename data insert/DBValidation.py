import sqlite3
import pandas as pd
import os

def validate_database(db_path, min_records=400):
    """
    Validate that all tables in the database have at least the specified number of records
    
    Parameters:
        db_path (str): Path to SQLite database
        min_records (int): Minimum number of records required in each table
        
    Returns:
        bool: True if all tables have at least min_records, False otherwise
    """
    try:
        # Connect to database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get list of tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        # Check record count for each table
        all_valid = True
        print("\n==== DATABASE VALIDATION RESULTS ====")
        print(f"Minimum required records per table: {min_records}")
        print("-" * 50)
        
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            status = "✓ PASS" if count >= min_records else "✗ FAIL"
            print(f"{table}: {count} records - {status}")
            
            if count < min_records:
                all_valid = False
        
        # Close connection
        conn.close()
        
        print("-" * 50)
        if all_valid:
            print("VALIDATION SUCCESSFUL: All tables have the required number of records.")
        else:
            print("VALIDATION FAILED: Some tables do not have the required number of records.")
        
        return all_valid
        
    except Exception as e:
        print(f"Error validating database: {str(e)}")
        return False

def generate_database_report(db_path, output_dir="database_report"):
    """
    Generate a detailed report of the database contents
    
    Parameters:
        db_path (str): Path to SQLite database
        output_dir (str): Directory to save report files
    """
    try:
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        # Connect to database
        conn = sqlite3.connect(db_path)
        
        # Get list of tables
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        # Create summary report
        report = []
        
        for table in tables:
            # Get column names
            cursor.execute(f"PRAGMA table_info({table})")
            columns = [row[1] for row in cursor.fetchall()]
            
            # Get record count
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            
            # Sample data (first 5 records)
            cursor.execute(f"SELECT * FROM {table} LIMIT 5")
            sample_data = cursor.fetchall()
            
            # Add to report
            report.append({
                "Table": table,
                "Columns": ", ".join(columns),
                "Record Count": count,
                "Sample Data": sample_data
            })
            
            # Export full table to CSV
            df = pd.read_sql_query(f"SELECT * FROM {table}", conn)
            df.to_csv(os.path.join(output_dir, f"{table}.csv"), index=False)
        
        # Create summary report
        with open(os.path.join(output_dir, "summary_report.txt"), "w") as f:
            f.write("DATABASE SUMMARY REPORT\n")
            f.write("======================\n\n")
            
            for table_info in report:
                f.write(f"Table: {table_info['Table']}\n")
                f.write(f"Columns: {table_info['Columns']}\n")
                f.write(f"Record Count: {table_info['Record Count']}\n")
                f.write("Sample Data:\n")
                
                for row in table_info['Sample Data']:
                    f.write(f"  {row}\n")
                
                f.write("\n" + "-" * 50 + "\n\n")
        
        # Close connection
        conn.close()
        
        print(f"\nDatabase report generated in '{output_dir}' directory.")
        
    except Exception as e:
        print(f"Error generating database report: {str(e)}")

def main():
    # Database path
    db_path = 'customer_database.db'
    
    # Check if database exists
    if not os.path.exists(db_path):
        print(f"Error: Database {db_path} does not exist.")
        return
    
    # Validate database
    is_valid = validate_database(db_path)
    
    # Generate report if validation is successful
    if is_valid:
        generate_database_report(db_path)
    
if __name__ == "__main__":
    main()