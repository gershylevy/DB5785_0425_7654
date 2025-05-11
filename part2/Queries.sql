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
-- Show customers with important notes in specific categories
SELECT 
    C.CustomerID, 
    C.Customer_First_Name, 
    C.Customer_Last_Name, 
    N.note_category,
    N.is_important
FROM 
    Customer C
JOIN 
    CustomerNote N ON C.CustomerID = N.customer_id
WHERE 
    N.is_important = TRUE
    AND N.note_category IN ('complain', 'report');


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
    C.Customer_Last_Name,
    A.city_name,
    A.street_address
FROM 
    Customer C
JOIN 
    Address A ON C.CustomerID = A.customer_id
WHERE 
    A.city_name = 'Longmen';




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
-- Remove customers who haven't been updated in over 3 years and have expired documents
DELETE FROM Customer
WHERE CustomerID IN (
    SELECT c.CustomerID
    FROM Customer c
    LEFT JOIN CustomerDocument d ON c.CustomerID = d.customer_id
    WHERE c.customer_since < CURRENT_DATE - INTERVAL '3 years'
    AND NOT EXISTS (
        SELECT 1
        FROM CustomerDocument
        WHERE customer_id = c.CustomerID
        AND expiry_date > CURRENT_DATE
    )
);



-- DELETE 2
-- Deletes non-primary addresses that are outside of Israel.
DELETE FROM Address
WHERE is_primary = FALSE AND country != 'Israel';

--DELETE 3 
-- Remove contact records that are duplicates but not marked as primary
DELETE FROM Contact
WHERE contactID IN (
    SELECT c1.contactID
    FROM Contact c1
    JOIN Contact c2 ON c1.customer_id = c2.customer_id 
        AND c1.contact_type = c2.contact_type
        AND c1.contact_value = c2.contact_value
    WHERE c1.is_primary = FALSE
    AND c2.is_primary = TRUE
);



-- UPDATE 1
--All notes (CustomerNote) belonging to customers over 65 years old will be marked as is_important = TRUE.
UPDATE CustomerNote
SET is_important = TRUE
WHERE customer_id IN (
    SELECT CustomerID FROM Customer 
    WHERE EXTRACT(YEAR FROM AGE(date_of_birth)) > 65
);

-- UPDATE 2
--Marks expired documents as unverified.
UPDATE CustomerDocument
SET verification_status = FALSE
WHERE expiry_date < CURRENT_DATE;

-- UPDATE 3
--Promotes customers with lots of valid documents to the Premium segment.
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

