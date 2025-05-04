
-- אילוץ CHECK לתאריך לידה בעתיד
ALTER TABLE Customer
ADD CONSTRAINT chk_birth_date CHECK (date_of_birth < CURRENT_DATE);

-- אילוץ DEFAULT לסוג כתובת
ALTER TABLE Address
ALTER COLUMN asress_type SET DEFAULT 'Home';

-- אילוץ NOT NULL לכתובת אימייל
ALTER TABLE Contact
ALTER COLUMN contact_value SET NOT NULL;
