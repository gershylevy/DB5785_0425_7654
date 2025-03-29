-- Create the Employee table (base table for both Manager and Subordinate)
CREATE TABLE Employee (
    EmployeeID VARCHAR2(20) PRIMARY KEY,
    Name VARCHAR2(100) NOT NULL
);

-- Create the Manager table with 1:1 relationship to Employee
CREATE TABLE Manager (
    EmployeeID VARCHAR2(20) PRIMARY KEY,
    OfficeNumber VARCHAR2(20) NOT NULL,
    Benefits VARCHAR2(255),
    FOREIGN KEY (EmployeeID) REFERENCES Employee(EmployeeID)
);

-- Create the Department table with reference to the Manager
CREATE TABLE Department (
    DepartmentID VARCHAR2(20) PRIMARY KEY,
    Name VARCHAR2(100) NOT NULL,
    Location VARCHAR2(100) NOT NULL,
    ManagerID VARCHAR2(20) NOT NULL,
    FOREIGN KEY (ManagerID) REFERENCES Manager(EmployeeID)
);

-- Create the Subordinate table with 1:1 relationship to Employee
CREATE TABLE Subordinate (
    EmployeeID VARCHAR2(20) PRIMARY KEY,
    DeskNumber VARCHAR2(20) NOT NULL,
    TimeAtJob INT NOT NULL, -- Assuming this is stored in months or years
    DepartmentID VARCHAR2(20) NOT NULL,
    FOREIGN KEY (EmployeeID) REFERENCES Employee(EmployeeID),
    FOREIGN KEY (DepartmentID) REFERENCES Department(DepartmentID)
);

-- Create the Payroll table
CREATE TABLE Payroll (
    PayrollID INT PRIMARY KEY,
    EmployeeID VARCHAR2(20) NOT NULL,
    Salary DECIMAL(10, 2) NOT NULL,
    PaymentFrequency VARCHAR2(20) NOT NULL, -- e.g., 'Monthly', 'Bi-weekly'
    FOREIGN KEY (EmployeeID) REFERENCES Employee(EmployeeID),
    UNIQUE (EmployeeID) -- Ensures the 1:1 relationship between Employee and Payroll
);

-- Create an ISA relationship table for tracking the type of employee
-- This is an alternative approach to implement the ISA relationship shown in the diagram
CREATE TABLE EmployeeType (
    EmployeeID VARCHAR2(20) PRIMARY KEY,
    Type VARCHAR2(20) CHECK (Type IN ('Manager', 'Subordinate')) NOT NULL,
    FOREIGN KEY (EmployeeID) REFERENCES Employee(EmployeeID)
);