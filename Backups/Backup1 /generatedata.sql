-- backup2.sql - Complete backup file for Customer Database

-- Create Customer table
CREATE TABLE Customer (
    CustomerID INT PRIMARY KEY,
    Customer_First_Name VARCHAR(50),
    Customer_Last_Name VARCHAR(50),
    ssn VARCHAR(20) UNIQUE,
    date_of_birth DATE,
    customer_since DATE
);

-- Create Address table (fixed typo in address_type column)
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
    employee_id INT,  -- Assuming employees exist in another table
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

-- Insert sample Customer records
INSERT INTO Customer (CustomerID, Customer_First_Name, Customer_Last_Name, ssn, date_of_birth, customer_since) VALUES 
(1, 'David', 'Cohen', '123-45-6789', '1985-06-15', '2018-03-12'),
(2, 'Sarah', 'Levi', '234-56-7890', '1990-11-22', '2019-07-30'),
(3, 'Moshe', 'Friedman', '345-67-8901', '1978-04-03', '2015-01-05'),
(4, 'Rachel', 'Goldberg', '456-78-9012', '1982-09-18', '2017-05-22'),
(5, 'Yael', 'Katz', '567-89-0123', '1995-02-27', '2020-11-14');

-- Insert sample Address records
INSERT INTO Address (addressID, customer_id, street_address, city_name, state, zip_code, country, address_type, is_primary) VALUES 
(1, 1, '123 Herzl St', 'Tel Aviv', 'Tel Aviv District', '6123456', 'Israel', 'Home', 1),
(2, 1, '45 Ben Yehuda St', 'Tel Aviv', 'Tel Aviv District', '6198765', 'Israel', 'Work', 0),
(3, 2, '78 Rothschild Blvd', 'Tel Aviv', 'Tel Aviv District', '6123789', 'Israel', 'Home', 1),
(4, 3, '12 Begin Rd', 'Jerusalem', 'Jerusalem District', '9104563', 'Israel', 'Home', 1),
(5, 4, '35 Dizengoff St', 'Tel Aviv', 'Tel Aviv District', '6143210', 'Israel', 'Home', 1);

-- Insert sample Contact records
INSERT INTO Contact (contactID, customer_id, contact_type, contact_value, is_primary) VALUES 
(1, 1, 'Email', 'david.cohen@example.com', 1),
(2, 1, 'Mobile', '+972-54-1234567', 1),
(3, 2, 'Email', 'sarah.levi@example.com', 1),
(4, 2, 'Phone', '+972-3-9876543', 0),
(5, 3, 'Email', 'moshe.friedman@example.com', 1);

-- Insert sample CustomerDocument records
INSERT INTO CustomerDocument (document_id, customer_id, document_type, document_number, issue_date, expiry_date, verification_status, file_reference) VALUES 
(1, 1, 'ID Card', 'ID-123456789', '2015-05-10', '2025-05-09', 1, 'DOC_1_IDCard_1.pdf'),
(2, 1, 'Passport', 'PS-12345678', '2018-07-22', '2028-07-21', 1, 'DOC_1_Passport_2.pdf'),
(3, 2, 'ID Card', 'ID-234567890', '2017-03-14', '2027-03-13', 1, 'DOC_2_IDCard_3.pdf'),
(4, 3, 'Driver License', 'DL-34567890', '2019-11-05', '2029-11-04', 1, 'DOC_3_DriverLicense_4.pdf'),
(5, 4, 'ID Card', 'ID-345678901', '2016-09-30', '2026-09-29', 1, 'DOC_4_IDCard_5.pdf');

-- Insert sample CustomerNote records
INSERT INTO CustomerNote (note_id, customer_id, employee_id, note_date, note_category, note_text, is_important) VALUES 
(1, 1, 10, '2021-06-15', 'Inquiry', 'Customer called about account access. Reset credentials.', 0),
(2, 1, 12, '2022-02-22', 'Request', 'Customer requested credit limit increase. Submitted application.', 1),
(3, 2, 8, '2021-09-03', 'Complaint', 'Customer reported unexpected fee. Refunded and explained policy.', 1),
(4, 3, 15, '2022-04-18', 'Update', 'Updated customer contact information upon request.', 0),
(5, 4, 7, '2022-01-27', 'Feedback', 'Customer provided positive feedback about new mobile app features.', 0);

-- Insert sample CustomerSegment records
INSERT INTO CustomerSegment (segment_id, segment_name, description, min_balance_required) VALUES 
(1, 'Premium', 'High-value customers with significant assets', 50000.00),
(2, 'Standard', 'Regular customers with moderate financial activity', 5000.00),
(3, 'Basic', 'Entry-level customers with minimal financial activity', 500.00),
(4, 'Student', 'Young customers with educational focus', 100.00),
(5, 'Senior', 'Customers over 65 with retirement needs', 1000.00);

-- Insert sample CustomerSegmentAssignment records
INSERT INTO CustomerSegmentAssignment (assignment_id, customer_id, segment_id, assigned_date) VALUES 
(1, 1, 1, '2019-05-20'),
(2, 2, 2, '2020-03-15'),
(3, 3, 1, '2018-11-12'),
(4, 4, 3, '2021-07-08'),
(5, 5, 4, '2022-01-30');

