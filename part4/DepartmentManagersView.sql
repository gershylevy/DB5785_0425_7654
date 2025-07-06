CREATE VIEW DepartmentManagersView AS
SELECT
    d.dept_id,
    d.dept_name,
    d.budget,
    e.EmployeeID AS manager_id,
    e.name AS manager_name,
    e.salary AS manager_salary
FROM Department d
JOIN Employee e ON d.manager_id = e.EmployeeID;
