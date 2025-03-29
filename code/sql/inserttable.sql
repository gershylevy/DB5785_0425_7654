-- Insert sample data into the Employee table
INSERT INTO Employee (EmployeeID, Name) VALUES
('E001', 'John Smith'),
('E002', 'Jane Doe'),
('E003', 'Robert Johnson'),
('E004', 'Maria Garcia'),
('E005', 'David Lee'),
('E006', 'Sarah Wilson'),
('E007', 'Michael Brown'),
('E008', 'Lisa Taylor');

-- Insert data into the Manager table
INSERT INTO Manager (EmployeeID, OfficeNumber, Benefits) VALUES
('E001', 'A101', 'Health, Dental, 401k, Stock Options'),
('E005', 'B202', 'Health, Dental, 401k'),
('E007', 'C303', 'Health, Vision, 401k, Company Car');

-- Insert data into the Department table
INSERT INTO Department (DepartmentID, Name, Location, ManagerID) VALUES
('D001', 'Engineering', 'Building A, Floor 2', 'E001'),
('D002', 'Marketing', 'Building B, Floor 1', 'E005'),
('D003', 'Finance', 'Building A, Floor 3', 'E007');

-- Insert data into the Subordinate table
INSERT INTO Subordinate (EmployeeID, DeskNumber, TimeAtJob, DepartmentID) VALUES
('E002', 'A123', 36, 'D001'),  -- 36 months in Engineering
('E003', 'A124', 24, 'D001'),  -- 24 months in Engineering
('E004', 'B125', 18, 'D002'),  -- 18 months in Marketing
('E006', 'A126', 12, 'D001'),  -- 12 months in Engineering
('E008', 'C127', 48, 'D003');  -- 48 months in Finance

-- Insert data into the Payroll table
INSERT INTO Payroll (EmployeeID, Salary, PaymentFrequency) VALUES
('E001', 120000.00, 'Monthly'),
('E002', 75000.00, 'Bi-weekly'),
('E003', 78000.00, 'Bi-weekly'),
('E004', 82000.00, 'Bi-weekly'),
('E005', 110000.00, 'Monthly'),
('E006', 76000.00, 'Bi-weekly'),
('E007', 125000.00, 'Monthly'),
('E008', 85000.00, 'Bi-weekly');

-- Insert data into the EmployeeType table
INSERT INTO EmployeeType (EmployeeID, Type) VALUES
('E001', 'Manager'),
('E002', 'Subordinate'),
('E003', 'Subordinate'),
('E004', 'Subordinate'),
('E005', 'Manager'),
('E006', 'Subordinate'),
('E007', 'Manager'),
('E008', 'Subordinate');