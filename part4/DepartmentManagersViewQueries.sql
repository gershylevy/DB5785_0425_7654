--- Query 1
--- Show all departments with budgets above 20,000 and a manager with salary 10,000

SELECT *
FROM DepartmentManagersView
WHERE budget > 20000 AND manager_salary > 10000;


--- Query 2
--- Sorts departments by highest salaray

SELECT dept_name, manager_name, manager_salary
FROM DepartmentManagersView
ORDER BY manager_salary DESC;
