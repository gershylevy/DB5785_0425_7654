
-- Customer: Prevents inserting or updating a customer with a future birth date.
ALTER TABLE Customer
ADD CONSTRAINT chk_birth_date CHECK (date_of_birth < CURRENT_DATE);

-- Address.address_type: Sets the default address type to 'Home' when none is provided.
ALTER TABLE Address
ALTER COLUMN asress_type SET DEFAULT 'Home';

-- Contact.contact_value: Ensures every contact must have a non-null email or phone value.
ALTER TABLE Contact
ALTER COLUMN contact_value SET NOT NULL;
