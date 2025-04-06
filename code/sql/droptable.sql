-- Disable foreign key checks to avoid dependency issues

SET FOREIGN_KEY_CHECKS = 0;



-- Drop tables in reverse order of dependencies

DROP TABLE IF EXISTS CustomerSegmentAssignment;

DROP TABLE IF EXISTS CustomerSegment;

DROP TABLE IF EXISTS CustomerNote;

DROP TABLE IF EXISTS CustomerDocument;

DROP TABLE IF EXISTS Contact;

DROP TABLE IF EXISTS Address;

DROP TABLE IF EXISTS Customer;



-- Re-enable foreign key checks

SET FOREIGN_KEY_CHECKS = 1;