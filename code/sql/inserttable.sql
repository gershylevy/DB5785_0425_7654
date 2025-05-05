-- Insert data into Customer table
INSERT INTO Customer (CustomerID, Customer_First_Name, Customer_Last_Name, ssn, date_of_birth, customer_since)
VALUES 
    (1001, 'John', 'Smith', '123-45-6789', '1985-04-12', '2020-01-15'),
    (1002, 'Mary', 'Johnson', '234-56-7890', '1992-08-23', '2019-05-20'),
    (1003, 'Robert', 'Williams', '345-67-8901', '1978-11-05', '2021-03-10'),
    (1004, 'Jennifer', 'Brown', '456-78-9012', '1990-02-28', '2018-09-05'),
    (1005, 'Michael', 'Jones', '567-89-0123', '1982-07-19', '2022-02-01');

-- Insert data into Address table
INSERT INTO Address (addressID, customer_id, street_address, city_name, state, zip_code, country, asress_type, is_primary)
VALUES 
    (101, 1001, '123 Main St', 'New York', 'NY', '10001', 'USA', 'HOME', TRUE),
    (102, 1001, '456 Business Ave', 'New York', 'NY', '10002', 'USA', 'WORK', FALSE),
    (103, 1002, '789 Park Rd', 'Los Angeles', 'CA', '90001', 'USA', 'HOME', TRUE),
    (104, 1003, '234 Oak St', 'Chicago', 'IL', '60601', 'USA', 'HOME', TRUE),
    (105, 1004, '567 Pine Ave', 'Miami', 'FL', '33101', 'USA', 'HOME', TRUE),
    (106, 1004, '890 Beach Blvd', 'Miami', 'FL', '33102', 'USA', 'VACATION', FALSE),
    (107, 1005, '321 Maple Dr', 'Seattle', 'WA', '98101', 'USA', 'HOME', TRUE);

-- Insert data into Contact table
INSERT INTO Contact (contactID, customer_id, contact_type, contact_value, is_primary)
VALUES 
    (201, 1001, 'EMAIL', 'john.smith@email.com', TRUE),
    (202, 1001, 'PHONE', '212-555-1234', FALSE),
    (203, 1002, 'EMAIL', 'mary.johnson@email.com', TRUE),
    (204, 1002, 'PHONE', '310-555-2345', TRUE),
    (205, 1003, 'EMAIL', 'robert.williams@email.com', TRUE),
    (206, 1003, 'PHONE', '312-555-3456', FALSE),
    (207, 1004, 'EMAIL', 'jennifer.brown@email.com', TRUE),
    (208, 1004, 'PHONE', '305-555-4567', TRUE),
    (209, 1005, 'EMAIL', 'michael.jones@email.com', TRUE),
    (210, 1005, 'PHONE', '206-555-5678', TRUE);

-- Insert data into CustomerDocument table
INSERT INTO CustomerDocument (document_id, customer_id, document_type, document_number, issue_date, expiry_date, verification_status, file_reference)
VALUES 
    (301, 1001, 'PASSPORT', 'P12345678', '2019-03-15', '2029-03-14', TRUE, 'documents/1001/passport.pdf'),
    (302, 1001, 'DRIVERS_LICENSE', 'DL98765432', '2021-05-20', '2025-05-19', TRUE, 'documents/1001/license.pdf'),
    (303, 1002, 'PASSPORT', 'P23456789', '2018-07-10', '2028-07-09', TRUE, 'documents/1002/passport.pdf'),
    (304, 1003, 'DRIVERS_LICENSE', 'DL87654321', '2020-01-30', '2024-01-29', TRUE, 'documents/1003/license.pdf'),
    (305, 1004, 'PASSPORT', 'P34567890', '2022-04-05', '2032-04-04', FALSE, 'documents/1004/passport.pdf'),
    (306, 1005, 'DRIVERS_LICENSE', 'DL76543210', '2021-09-18', '2025-09-17', TRUE, 'documents/1005/license.pdf');

-- Insert data into CustomerNote table
INSERT INTO CustomerNote (note_id, customer_id, employee_id, note_date, note_category, note_text, is_important)
VALUES 
    (401, 1001, 501, '2022-02-10', 'ACCOUNT_REVIEW', 'Customer requested information about investment options.', FALSE),
    (402, 1001, 502, '2022-05-15', 'COMPLAINT', 'Customer reported issues with online banking access.', TRUE),
    (403, 1002, 503, '2022-03-20', 'ACCOUNT_REVIEW', 'Annual account review completed. No issues found.', FALSE),
    (404, 1003, 501, '2022-04-12', 'INQUIRY', 'Customer asked about mortgage refinancing options.', FALSE),
    (405, 1004, 504, '2022-06-05', 'COMPLAINT', 'Customer experienced delay in fund transfer.', TRUE),
    (406, 1005, 502, '2022-07-18', 'ACCOUNT_REVIEW', 'Customer upgraded to premium service package.', FALSE);

-- Insert data into CustomerSegment table
INSERT INTO CustomerSegment (segment_id, segment_name, description, min_balance_required)
VALUES 
    (601, 'STANDARD', 'Regular customers with basic services', 0.00),
    (602, 'PREMIUM', 'Customers with higher balances and enhanced services', 10000.00),
    (603, 'GOLD', 'High-value customers with premium services and dedicated support', 50000.00),
    (604, 'PLATINUM', 'Top-tier customers with exclusive benefits and personalized service', 100000.00);

-- Insert data into CustomerSegmentAssignment table
INSERT INTO CustomerSegmentAssignment (assignment_id, customer_id, segment_id, assigned_date)
VALUES 
    (701, 1001, 602, '2022-01-01'),
    (702, 1002, 601, '2021-06-15'),
    (703, 1003, 601, '2021-03-10'),
    (704, 1004, 603, '2020-10-20'),
    (705, 1005, 604, '2022-02-01');
