-- Drop tables in correct order to handle foreign key constraints properly
-- First drop tables that have the most dependencies on other tables

-- Drop the EmployeeType table
DROP TABLE IF EXISTS EmployeeType;

-- Drop the Payroll table
DROP TABLE IF EXISTS Payroll;

-- Drop the Subordinate table (depends on Employee and Department)
DROP TABLE IF EXISTS Subordinate;

-- Drop the Department table (depends on Manager)
DROP TABLE IF EXISTS Department;

-- Drop the Manager table (depends on Employee)
DROP TABLE IF EXISTS Manager;

-- Finally drop the base Employee table (no dependencies)
DROP TABLE IF EXISTS Employee;