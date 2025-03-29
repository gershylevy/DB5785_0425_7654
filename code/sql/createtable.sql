-- Create the Employee table (base table for both Manager and Subordinate)
CREATE TABLE Employee (
    EmployeeID VARCHAR(20) PRIMARY KEY,
    Name VARCHAR(100) NOT NULL
);

-- Create the Manager table with 1:1 relationship to Employee
CREATE TABLE Manager (
    EmployeeID VARCHAR(20) PRIMARY KEY,
    OfficeNumber VARCHAR(20) NOT NULL,
    Benefits VARCHAR(255),
    FOREIGN KEY (EmployeeID) REFERENCES Employee(EmployeeID)
);

-- Create the Department table with reference to the Manager
CREATE TABLE Department (
    DepartmentID VARCHAR(20) PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Location VARCHAR(100) NOT NULL,
    ManagerID VARCHAR(20) NOT NULL,
    FOREIGN KEY (ManagerID) REFERENCES Manager(EmployeeID)
);

-- Create the Subordinate table with 1:1 relationship to Employee
CREATE TABLE Subordinate (
    EmployeeID VARCHAR(20) PRIMARY KEY,
    DeskNumber VARCHAR(20) NOT NULL,
    TimeAtJob INT NOT NULL, -- Assuming this is stored in months or years
    DepartmentID VARCHAR(20) NOT NULL,
    FOREIGN KEY (EmployeeID) REFERENCES Employee(EmployeeID),
    FOREIGN KEY (DepartmentID) REFERENCES Department(DepartmentID)
);

-- Create the Payroll table
CREATE TABLE Payroll (
    PayrollID INT PRIMARY KEY AUTO_INCREMENT,
    EmployeeID VARCHAR(20) NOT NULL,
    Salary DECIMAL(10, 2) NOT NULL,
    PaymentFrequency VARCHAR(20) NOT NULL, -- e.g., 'Monthly', 'Bi-weekly'
    FOREIGN KEY (EmployeeID) REFERENCES Employee(EmployeeID),
    UNIQUE (EmployeeID) -- Ensures the 1:1 relationship between Employee and Payroll
);

-- Create an ISA relationship table for tracking the type of employee
-- This is an alternative approach to implement the ISA relationship shown in the diagram
CREATE TABLE EmployeeType (
    EmployeeID VARCHAR(20) PRIMARY KEY,
    Type ENUM('Manager', 'Subordinate') NOT NULL,
    FOREIGN KEY (EmployeeID) REFERENCES Employee(EmployeeID)
);