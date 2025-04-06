import sqlite3
import random
from datetime import datetime
import string
import os

# Create a connection to the database
# Replace 'employee_database.db' with your actual database file path
conn = sqlite3.connect('employee_database.db')
cursor = conn.cursor()

# Function to generate a random string of given length
def random_string(length):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(length))

# Function to generate random names
def generate_name():
    first_names = ["James", "John", "Robert", "Michael", "William", "David", "Richard", "Joseph", "Thomas", "Charles",
                  "Mary", "Patricia", "Jennifer", "Linda", "Elizabeth", "Barbara", "Susan", "Jessica", "Sarah", "Karen",
                  "Daniel", "Matthew", "Anthony", "Mark", "Donald", "Steven", "Paul", "Andrew", "Joshua", "Kenneth",
                  "Lisa", "Nancy", "Betty", "Sandra", "Margaret", "Ashley", "Kimberly", "Emily", "Donna", "Michelle",
                  "Yael", "Avi", "Moshe", "Sarah", "David", "Yosef", "Rachel", "Yaakov", "Miriam", "Shlomo"]
    
    last_names = ["Smith", "Johnson", "Williams", "Jones", "Brown", "Davis", "Miller", "Wilson", "Moore", "Taylor",
                 "Anderson", "Thomas", "Jackson", "White", "Harris", "Martin", "Thompson", "Garcia", "Martinez", "Robinson",
                 "Clark", "Rodriguez", "Lewis", "Lee", "Walker", "Hall", "Allen", "Young", "Hernandez", "King",
                 "Wright", "Lopez", "Hill", "Scott", "Green", "Adams", "Baker", "Gonzalez", "Nelson", "Carter",
                 "Cohen", "Levi", "Friedman", "Goldberg", "Schwartz", "Katz", "Rosenberg", "Shapiro", "Rubinstein", "Kaplan"]
    
    return f"{random.choice(first_names)} {random.choice(last_names)}"

# Function to generate random office/desk number
def generate_location_number():
    building = random.choice(["A", "B", "C", "D"])
    floor = random.randint(1, 5)
    room = random.randint(100, 999)
    return f"{building}{floor}{room}"

# Function to generate random benefits
def generate_benefits():
    benefits = ["Health", "Dental", "Vision", "401k", "Stock Options", "Company Car", "Life Insurance", 
                "Disability Insurance", "Paid Time Off", "Fitness Membership", "Education Reimbursement"]
    num_benefits = random.randint(2, 5)
    selected_benefits = random.sample(benefits, num_benefits)
    return ", ".join(selected_benefits)

# Function to generate random payment frequency
def generate_payment_frequency():
    return random.choice(["Monthly", "Bi-weekly", "Weekly"])

# Function to generate random salary based on employee type
def generate_salary(emp_type):
    if emp_type == "Manager":
        return round(random.uniform(90000, 150000), 2)
    else:
        return round(random.uniform(60000, 95000), 2)

# Function to generate department data
def generate_departments(num_departments):
    departments = []
    locations = ["Building A, Floor 1", "Building A, Floor 2", "Building A, Floor 3", 
                 "Building B, Floor 1", "Building B, Floor 2", "Building C, Floor 1", 
                 "Building D, Floor 1", "Building D, Floor 2", "Building D, Floor 3"]
    
    department_names = [
        "Engineering", "Marketing", "Finance", "Human Resources", "Research and Development",
        "Sales", "Customer Support", "Information Technology", "Operations", "Legal",
        "Product Management", "Quality Assurance", "Business Development", "Administration",
        "Public Relations", "Supply Chain", "Manufacturing", "Design", "Analytics", "Security"
    ]
    
    # Make sure we don't exceed available department names
    num_departments = min(num_departments, len(department_names))
    
    selected_dept_names = random.sample(department_names, num_departments)
    
    for i in range(num_departments):
        dept_id = f"D{str(i+1).zfill(3)}"
        departments.append({
            "DepartmentID": dept_id,
            "Name": selected_dept_names[i],
            "Location": random.choice(locations)
        })
    
    return departments

# Clear existing data (if any)
try:
    cursor.execute("DELETE FROM EmployeeType")
    cursor.execute("DELETE FROM Payroll")
    cursor.execute("DELETE FROM Subordinate")
    cursor.execute("DELETE FROM Department")
    cursor.execute("DELETE FROM Manager")
    cursor.execute("DELETE FROM Employee")
    conn.commit()
except sqlite3.Error as e:
    print(f"Error clearing tables: {e}")
    conn.rollback()

# Configuration
num_employees = 450  # Total employees
manager_percentage = 0.15  # 15% of employees are managers
num_departments = 20

# Generate department data without managers initially
departments = generate_departments(num_departments)

# Generate employee data
employees = []
managers = []
subordinates = []
payrolls = []
employee_types = []

# First create all employees
for i in range(num_employees):
    emp_id = f"E{str(i+1).zfill(3)}"
    name = generate_name()
    
    employees.append({
        "EmployeeID": emp_id,
        "Name": name
    })
    
    # Determine if this employee is a manager
    is_manager = random.random() < manager_percentage
    emp_type = "Manager" if is_manager else "Subordinate"
    
    employee_types.append({
        "EmployeeID": emp_id,
        "Type": emp_type
    })
    
    # Create payroll record
    payrolls.append({
        "EmployeeID": emp_id,
        "Salary": generate_salary(emp_type),
        "PaymentFrequency": generate_payment_frequency()
    })
    
    # Add to appropriate role list
    if is_manager:
        managers.append({
            "EmployeeID": emp_id,
            "OfficeNumber": generate_location_number(),
            "Benefits": generate_benefits()
        })
    else:
        # Subordinate information will be completed after departments are assigned managers
        subordinates.append({
            "EmployeeID": emp_id,
            "DeskNumber": generate_location_number(),
            "TimeAtJob": random.randint(1, 120)  # 1 to 120 months
        })

# Assign managers to departments
manager_ids = [m["EmployeeID"] for m in managers]
random.shuffle(manager_ids)

for i, dept in enumerate(departments):
    if i < len(manager_ids):
        dept["ManagerID"] = manager_ids[i]
    else:
        # If we run out of managers, reuse existing ones
        dept["ManagerID"] = random.choice(manager_ids)

# Now assign departments to subordinates
for sub in subordinates:
    sub["DepartmentID"] = random.choice(departments)["DepartmentID"]

# Insert data into tables
try:
    # Insert Employees
    cursor.executemany(
        "INSERT INTO Employee (EmployeeID, Name) VALUES (:EmployeeID, :Name)",
        employees
    )
    
    # Insert Managers
    cursor.executemany(
        "INSERT INTO Manager (EmployeeID, OfficeNumber, Benefits) VALUES (:EmployeeID, :OfficeNumber, :Benefits)",
        managers
    )
    
    # Insert Departments
    cursor.executemany(
        "INSERT INTO Department (DepartmentID, Name, Location, ManagerID) VALUES (:DepartmentID, :Name, :Location, :ManagerID)",
        departments
    )
    
    # Insert Subordinates
    cursor.executemany(
        "INSERT INTO Subordinate (EmployeeID, DeskNumber, TimeAtJob, DepartmentID) VALUES (:EmployeeID, :DeskNumber, :TimeAtJob, :DepartmentID)",
        subordinates
    )
    
    # Insert Payrolls
    cursor.executemany(
        "INSERT INTO Payroll (EmployeeID, Salary, PaymentFrequency) VALUES (:EmployeeID, :Salary, :PaymentFrequency)",
        payrolls
    )
    
    # Insert EmployeeTypes
    cursor.executemany(
        "INSERT INTO EmployeeType (EmployeeID, Type) VALUES (:EmployeeID, :Type)",
        employee_types
    )
    
    conn.commit()
    print(f"Successfully inserted: {len(employees)} employees ({len(managers)} managers, {len(subordinates)} subordinates), {len(departments)} departments")
    
except sqlite3.Error as e:
    print(f"Error inserting data: {e}")
    conn.rollback()

# Create backup function
def backup_database(source_db, backup_dir="backups"):
    # Create backups directory if it doesn't exist
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    
    # Generate backup filename with current date
    current_date = datetime.now().strftime("%Y%m%d")
    backup_file = f"{backup_dir}/backup_{current_date}.db"
    
    # Connect to source database
    source_conn = sqlite3.connect(source_db)
    
    # Connect to backup database
    backup_conn = sqlite3.connect(backup_file)
    
    # Backup
    source_conn.backup(backup_conn)
    
    # Close connections
    source_conn.close()
    backup_conn.close()
    
    print(f"Database backed up to {backup_file}")
    return backup_file

# Uncomment to create backup
# backup_file = backup_database('employee_database.db')

# Close the database connection
conn.close()