-- Comprehensive join of all tables
SELECT e.EmployeeID, e.Name, et.Type AS EmployeeType, 
       p.Salary, p.PaymentFrequency,
       CASE 
           WHEN et.Type = 'Manager' THEN m.OfficeNumber 
           WHEN et.Type = 'Subordinate' THEN s.DeskNumber
           ELSE NULL
       END AS OfficeOrDeskNumber,
       CASE 
           WHEN et.Type = 'Manager' THEN m.Benefits
           ELSE NULL
       END AS Benefits,
       CASE 
           WHEN et.Type = 'Subordinate' THEN s.TimeAtJob
           ELSE NULL
       END AS TimeAtJob,
       CASE 
           WHEN et.Type = 'Subordinate' THEN d.Name
           ELSE NULL
       END AS BelongsToDepartment,
       CASE 
           WHEN et.Type = 'Manager' THEN 
               (SELECT GROUP_CONCAT(d2.Name) FROM Department d2 WHERE d2.ManagerID = e.EmployeeID)
           ELSE NULL
       END AS ManagesDepartments
FROM Employee e
LEFT JOIN Manager m ON e.EmployeeID = m.EmployeeID
LEFT JOIN Subordinate s ON e.EmployeeID = s.EmployeeID
LEFT JOIN Department d ON s.DepartmentID = d.DepartmentID
JOIN Payroll p ON e.EmployeeID = p.EmployeeID
JOIN EmployeeType et ON e.EmployeeID = et.EmployeeID;