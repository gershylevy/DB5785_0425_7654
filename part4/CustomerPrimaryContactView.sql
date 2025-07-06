CREATE VIEW CustomerPrimaryContactView AS
SELECT
    c.CustomerID,
    c.Customer_First_Name,
    c.Customer_Last_Name,
    c.customer_since,
    ct.contact_type,
    ct.contact_value
FROM Customer c
JOIN Contact ct ON c.CustomerID = ct.customer_id
WHERE ct.is_primary = TRUE;
