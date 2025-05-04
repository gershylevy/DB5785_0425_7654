
-- SELECT 1
SELECT 
    C.Customer_First_Name, 
    C.Customer_Last_Name, 
    COUNT(D.document_id) AS ValidDocuments
FROM 
    Customer C
JOIN 
    CustomerDocument D ON C.CustomerID = D.customer_id
WHERE 
    D.expiry_date > CURRENT_DATE
GROUP BY 
    C.CustomerID;

-- SELECT 2
SELECT 
    C.Customer_First_Name, 
    C.Customer_Last_Name,
    A.street_address, 
    A.city_name
FROM 
    Customer C
JOIN 
    Address A ON C.CustomerID = A.customer_id
WHERE 
    A.is_primary = TRUE
    AND EXTRACT(YEAR FROM C.customer_since) = EXTRACT(YEAR FROM CURRENT_DATE);

-- SELECT 3
SELECT 
    C.CustomerID, 
    C.Customer_First_Name, 
    C.Customer_Last_Name, 
    COUNT(N.note_id) AS ImportantNotes
FROM 
    Customer C
JOIN 
    CustomerNote N ON C.CustomerID = N.customer_id
WHERE 
    N.is_important = TRUE
GROUP BY 
    C.CustomerID
HAVING 
    COUNT(N.note_id) > 1;

-- SELECT 4
SELECT 
    C.Customer_First_Name, 
    C.Customer_Last_Name,
    CT.contact_type, 
    CT.contact_value
FROM 
    Customer C
JOIN 
    Contact CT ON C.CustomerID = CT.customer_id
WHERE 
    CT.is_primary = TRUE
ORDER BY 
    CT.contact_type;

-- SELECT 5
SELECT 
    C.CustomerID, 
    C.Customer_First_Name, 
    C.Customer_Last_Name
FROM 
    Customer C
LEFT JOIN 
    Address A ON C.CustomerID = A.customer_id
WHERE 
    A.customer_id IS NULL;

-- SELECT 6
SELECT 
    S.segment_name, 
    ROUND(AVG(EXTRACT(YEAR FROM AGE(C.date_of_birth))), 1) AS avg_age
FROM 
    CustomerSegmentAssignment A
JOIN 
    Customer C ON C.CustomerID = A.customer_id
JOIN 
    CustomerSegment S ON S.segment_id = A.segment_id
GROUP BY 
    S.segment_name;

-- SELECT 7
SELECT 
    C.CustomerID, 
    C.Customer_First_Name, 
    C.Customer_Last_Name,
    D.document_type, 
    D.expiry_date
FROM 
    Customer C
JOIN 
    CustomerDocument D ON C.CustomerID = D.customer_id
WHERE 
    D.expiry_date < CURRENT_DATE - INTERVAL '1 year';

-- SELECT 8
SELECT 
    EXTRACT(MONTH FROM customer_since) AS month, 
    COUNT(*) AS customer_count
FROM 
    Customer
GROUP BY 
    EXTRACT(MONTH FROM customer_since)
ORDER BY 
    month;

-- DELETE 1
DELETE FROM Customer
WHERE CustomerID NOT IN (
    SELECT customer_id FROM CustomerSegmentAssignment
);

-- DELETE 2
DELETE FROM Address
WHERE is_primary = FALSE AND country != 'Israel';

-- DELETE 3
DELETE FROM CustomerDocument
WHERE expiry_date < CURRENT_DATE - INTERVAL '5 years';

-- UPDATE 1
UPDATE CustomerNote
SET is_important = TRUE
WHERE customer_id IN (
    SELECT CustomerID FROM Customer 
    WHERE EXTRACT(YEAR FROM AGE(date_of_birth)) > 65
);

-- UPDATE 2
UPDATE CustomerDocument
SET verification_status = FALSE
WHERE expiry_date < CURRENT_DATE;

-- UPDATE 3
UPDATE CustomerSegmentAssignment
SET segment_id = (
    SELECT segment_id FROM CustomerSegment WHERE segment_name = 'Premium'
)
WHERE customer_id IN (
    SELECT customer_id FROM CustomerDocument
    WHERE expiry_date > CURRENT_DATE
    GROUP BY customer_id
    HAVING COUNT(document_id) > 3
);

-- ROLLBACK example
BEGIN;
UPDATE CustomerNote
SET note_text = 'בדיקה זמנית'
WHERE is_important = TRUE;
SELECT * FROM CustomerNote WHERE is_important = TRUE;
ROLLBACK;

-- COMMIT example
BEGIN;
UPDATE CustomerNote
SET note_text = 'עודכנה על ידי מערכת'
WHERE is_important = TRUE;
SELECT * FROM CustomerNote WHERE is_important = TRUE;
COMMIT;
SELECT * FROM CustomerNote WHERE is_important = TRUE;
