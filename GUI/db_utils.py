# db_utils.py - Database utilities and initialization
import psycopg2
import psycopg2.extras
from datetime import datetime, date, timedelta
import random
from faker import Faker
import sys

fake = Faker()

class DatabaseUtils:
    """Utility functions for database management"""
    
    def _init_(self, connection_params):
        self.connection_params = connection_params
        self.connection = None
        self.cursor = None
    
    def connect(self):
        """Establish database connection"""
        try:
            self.connection = psycopg2.connect(**self.connection_params)
            self.cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
            return True
        except Exception as e:
            print(f"Connection failed: {e}")
            return False
    
    def disconnect(self):
        """Close database connection"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
    
    def execute_sql_file(self, file_path):
        """Execute SQL commands from a file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                sql_commands = file.read()
                self.cursor.execute(sql_commands)
                self.connection.commit()
                print(f"✅ Successfully executed {file_path}")
                return True
        except Exception as e:
            print(f"❌ Error executing {file_path}: {e}")
            self.connection.rollback()
            return False
    
    def check_table_exists(self, table_name):
        """Check if a table exists"""
        try:
            self.cursor.execute("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_name = %s
                )
            """, (table_name.lower(),))
            return self.cursor.fetchone()[0]
        except Exception:
            return False
    
    def get_table_count(self, table_name):
        """Get row count for a table"""
        try:
            self.cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            return self.cursor.fetchone()[0]
        except Exception:
            return 0
    
    def create_tables(self):
        """Create all required tables"""
        create_sql = """
        -- Drop existing tables (if they exist) in correct order
        DROP TABLE IF EXISTS CustomerSegmentAssignment CASCADE;
        DROP TABLE IF EXISTS CustomerNote CASCADE;
        DROP TABLE IF EXISTS CustomerDocument CASCADE;
        DROP TABLE IF EXISTS Contact CASCADE;
        DROP TABLE IF EXISTS Address CASCADE;
        DROP TABLE IF EXISTS Customer CASCADE;
        DROP TABLE IF EXISTS CustomerSegment CASCADE;

        -- Create Customer table
        CREATE TABLE Customer (
            EmployeeID INT,
            CustomerID INT PRIMARY KEY,
            Customer_First_Name VARCHAR(50),
            Customer_Last_Name VARCHAR(50),
            ssn VARCHAR(20) UNIQUE,
            date_of_birth DATE,
            customer_since DATE
        );

        -- Create Address table
        CREATE TABLE Address (
            addressID INT PRIMARY KEY,
            customer_id INT,
            street_address VARCHAR(255),
            city_name VARCHAR(50),
            state VARCHAR(50),
            zip_code VARCHAR(20),
            country VARCHAR(50),
            asress_type VARCHAR(50),  -- Note: keeping original typo for compatibility
            is_primary BOOLEAN,
            FOREIGN KEY (customer_id) REFERENCES Customer(CustomerID) ON DELETE CASCADE
        );

        -- Create Contact table
        CREATE TABLE Contact (
            contactID INT PRIMARY KEY,
            customer_id INT,
            contact_type VARCHAR(50),
            contact_value VARCHAR(100),
            is_primary BOOLEAN,
            FOREIGN KEY (customer_id) REFERENCES Customer(CustomerID) ON DELETE CASCADE
        );

        -- Create CustomerDocument table
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

        -- Create CustomerNote table
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

        -- Create CustomerSegment table
        CREATE TABLE CustomerSegment (
            segment_id INT PRIMARY KEY,
            segment_name VARCHAR(100),
            description TEXT,
            min_balance_required DECIMAL(10,2)
        );

        -- Create CustomerSegmentAssignment table
        CREATE TABLE CustomerSegmentAssignment (
            assignment_id INT PRIMARY KEY,
            customer_id INT,
            segment_id INT,
            assigned_date DATE,
            FOREIGN KEY (customer_id) REFERENCES Customer(CustomerID) ON DELETE CASCADE,
            FOREIGN KEY (segment_id) REFERENCES CustomerSegment(segment_id) ON DELETE CASCADE
        );
        """
        
        try:
            self.cursor.execute(create_sql)
            self.connection.commit()
            print("✅ Tables created successfully")
            return True
        except Exception as e:
            print(f"❌ Error creating tables: {e}")
            self.connection.rollback()
            return False
    
    def create_segments(self):
        """Create customer segments"""
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
        
        try:
            for segment in segments:
                self.cursor.execute("""
                    INSERT INTO CustomerSegment (segment_id, segment_name, description, min_balance_required)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (segment_id) DO NOTHING
                """, segment)
            
            self.connection.commit()
            print(f"✅ Created {len(segments)} customer segments")
            return True
        except Exception as e:
            print(f"❌ Error creating segments: {e}")
            self.connection.rollback()
            return False
    
    def generate_sample_data(self, num_customers=50):
        """Generate sample data for testing"""
        print(f"Generating sample data for {num_customers} customers...")
        
        try:
            # Generate customers
            customers = []
            used_ssns = set()
            used_ids = set()
            
            for i in range(num_customers):
                # Generate unique customer ID
                while True:
                    customer_id = random.randint(1000, 9999)
                    if customer_id not in used_ids:
                        used_ids.add(customer_id)
                        break
                
                # Generate unique SSN
                while True:
                    ssn = f"{random.randint(100, 999)}-{random.randint(10, 99)}-{random.randint(1000, 9999)}"
                    if ssn not in used_ssns:
                        used_ssns.add(ssn)
                        break
                
                customer = (
                    random.randint(1, 10),  # employee_id
                    customer_id,
                    fake.first_name(),
                    fake.last_name(),
                    ssn,
                    fake.date_of_birth(minimum_age=18, maximum_age=90),
                    fake.date_between(start_date='-10y', end_date='today')
                )
                customers.append(customer)
            
            # Insert customers
            self.cursor.executemany("""
                INSERT INTO Customer (EmployeeID, CustomerID, Customer_First_Name, Customer_Last_Name, 
                                    ssn, date_of_birth, customer_since)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, customers)
            
            print(f"✅ Inserted {len(customers)} customers")
            
            # Generate addresses
            addresses = []
            address_id = 1
            address_types = ["Home", "Work", "Shipping", "Billing", "Secondary"]
            countries = ["Israel", "USA", "Canada", "UK", "Australia", "Germany", "France"]
            
            for customer in customers:
                customer_id = customer[1]
                num_addresses = random.randint(1, 3)
                
                for j in range(num_addresses):
                    address = (
                        address_id,
                        customer_id,
                        fake.street_address(),
                        fake.city(),
                        fake.state(),
                        fake.zipcode(),
                        random.choice(countries),
                        random.choice(address_types),
                        j == 0  # First address is primary
                    )
                    addresses.append(address)
                    address_id += 1
            
            self.cursor.executemany("""
                INSERT INTO Address (addressID, customer_id, street_address, city_name, 
                                   state, zip_code, country, asress_type, is_primary)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, addresses)
            
            print(f"✅ Inserted {len(addresses)} addresses")
            
            # Generate contacts
            contacts = []
            contact_id = 1
            contact_types = ["Email", "Phone", "Mobile", "Work Phone", "Fax"]
            
            for customer in customers:
                customer_id = customer[1]
                num_contacts = random.randint(1, 3)
                
                for j in range(num_contacts):
                    contact_type = random.choice(contact_types)
                    
                    if contact_type == "Email":
                        value = fake.email()
                    else:
                        value = fake.phone_number()
                    
                    contact = (
                        contact_id,
                        customer_id,
                        contact_type,
                        value,
                        j == 0  # First contact is primary
                    )
                    contacts.append(contact)
                    contact_id += 1
            
            self.cursor.executemany("""
                INSERT INTO Contact (contactID, customer_id, contact_type, contact_value, is_primary)
                VALUES (%s, %s, %s, %s, %s)
            """, contacts)
            
            print(f"✅ Inserted {len(contacts)} contacts")
            
            # Generate documents
            documents = []
            document_id = 1
            document_types = ["Passport", "Driver License", "ID Card", "Birth Certificate", "Social Security Card"]
            used_doc_numbers = set()
            
            for customer in customers:
                customer_id = customer[1]
                num_documents = random.randint(1, 3)
                
                for j in range(num_documents):
                    doc_type = random.choice(document_types)
                    
                    # Generate unique document number
                    while True:
                        doc_num = f"{doc_type[:2].upper()}-{random.randint(100000, 999999)}"
                        if doc_num not in used_doc_numbers:
                            used_doc_numbers.add(doc_num)
                            break
                    
                    issue_date = fake.date_between(start_date='-10y', end_date='-1y')
                    expiry_date = fake.date_between(start_date='+1y', end_date='+10y')
                    
                    document = (
                        document_id,
                        customer_id,
                        doc_type,
                        doc_num,
                        issue_date,
                        expiry_date,
                        random.choice([True, False]),  # verification_status
                        f"DOC_{customer_id}_{document_id}.pdf"
                    )
                    documents.append(document)
                    document_id += 1
            
            self.cursor.executemany("""
                INSERT INTO CustomerDocument (document_id, customer_id, document_type, 
                                            document_number, issue_date, expiry_date, 
                                            verification_status, file_reference)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, documents)
            
            print(f"✅ Inserted {len(documents)} documents")
            
            # Generate notes
            notes = []
            note_id = 1
            note_categories = ["Inquiry", "Complaint", "Request", "Feedback", "Update", "Alert"]
            note_templates = [
                "Customer called about account inquiry.",
                "Customer visited branch for service request.",
                "Follow-up needed on customer complaint.",
                "Customer provided positive feedback.",
                "Account information updated."
            ]
            
            for customer in customers:
                customer_id = customer[1]
                num_notes = random.randint(0, 3)
                
                for j in range(num_notes):
                    note = (
                        note_id,
                        customer_id,
                        random.randint(1, 10),  # employee_id
                        fake.date_between(start_date='-2y', end_date='today'),
                        random.choice(note_categories),
                        random.choice(note_templates),
                        random.choice([True, False])  # is_important
                    )
                    notes.append(note)
                    note_id += 1
            
            self.cursor.executemany("""
                INSERT INTO CustomerNote (note_id, customer_id, employee_id, note_date, 
                                        note_category, note_text, is_important)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, notes)
            
            print(f"✅ Inserted {len(notes)} notes")
            
            # Generate segment assignments
            assignments = []
            assignment_id = 1
            
            for customer in customers:
                customer_id = customer[1]
                segment_id = random.randint(1, 10)
                
                assignment = (
                    assignment_id,
                    customer_id,
                    segment_id,
                    fake.date_between(start_date='-3y', end_date='today')
                )
                assignments.append(assignment)
                assignment_id += 1
            
            self.cursor.executemany("""
                INSERT INTO CustomerSegmentAssignment (assignment_id, customer_id, 
                                                     segment_id, assigned_date)
                VALUES (%s, %s, %s, %s)
            """, assignments)
            
            print(f"✅ Inserted {len(assignments)} segment assignments")
            
            self.connection.commit()
            print("✅ Sample data generation completed successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Error generating sample data: {e}")
            self.connection.rollback()
            return False
    
    def get_database_summary(self):
        """Get summary of database contents"""
        tables = ['Customer', 'Address', 'Contact', 'CustomerDocument', 
                 'CustomerNote', 'CustomerSegment', 'CustomerSegmentAssignment']
        
        summary = "DATABASE SUMMARY\n" + "=" * 40 + "\n"
        
        for table in tables:
            if self.check_table_exists(table):
                count = self.get_table_count(table)
                summary += f"{table:<25}: {count:>8} records\n"
            else:
                summary += f"{table:<25}: Not found\n"
        
        return summary

def main():
    """Main function for database initialization"""
    print("Database Initialization Utility")
    print("=" * 40)
    
    # Connection parameters
    connection_params = {
        'host': 'localhost',
        'port': '5432',
        'database': 'postgres',
        'user': 'postgres',
        'password': input("Enter PostgreSQL password: ")
    }
    
    # Initialize database utils
    db_utils = DatabaseUtils(connection_params)
    
    if not db_utils.connect():
        print("Failed to connect to database. Exiting.")
        return
    
    try:
        print("\n1. Creating tables...")
        if db_utils.create_tables():
            print("✅ Tables created successfully")
        else:
            print("❌ Failed to create tables")
            return
        
        print("\n2. Creating customer segments...")
        if db_utils.create_segments():
            print("✅ Customer segments created")
        else:
            print("❌ Failed to create segments")
            return
        
        print("\n3. Generating sample data...")
        num_customers = int(input("Enter number of customers to generate (default: 50): ") or "50")
        
        if db_utils.generate_sample_data(num_customers):
            print("✅ Sample data generated successfully")
        else:
            print("❌ Failed to generate sample data")
            return
        
        print("\n4. Database summary:")
        print(db_utils.get_database_summary())
        
        print("\n✅ Database initialization completed successfully!")
        print("You can now run the GUI application: python customer_db_gui.py")
        
    finally:
        db_utils.disconnect()

if __name__ == "__main__":
    main()