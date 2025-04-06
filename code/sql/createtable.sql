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
    asress_type VARCHAR(50),  -- Assuming "asress_type" is a typo for "address_type"
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
    employee_id INT,  -- Assuming employees exist in another table
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