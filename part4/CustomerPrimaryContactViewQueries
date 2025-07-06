--- Query 1
--- Shows all costumers who joined after 2022 and have a phone contact type

SELECT *
FROM CustomerPrimaryContactView
WHERE customer_since > '2022-01-01'
  AND contact_type = 'Phone';


--- Query 2
--- Shows how many costumers per contact type

SELECT contact_type, COUNT(*) AS num_customers
FROM CustomerPrimaryContactView
GROUP BY contact_type;
