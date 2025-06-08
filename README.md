# 🧑‍💻 DB5785 - PostgreSQL and Docker Workshop 🗄️🐋

This workshop will guide you through setting up and managing a _PostgreSQL database_ using Docker.  
You will also explore how to use _pgAdmin_ GUI to interact with the database and perform various tasks.  

You will have to add to the [Workshop Files & Scripts](#workshop-id) section your own specific implementation  
- see: *[Markdown Guide](https://www.markdownguide.org)* and *[Writing and Formatting in Github](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github)* for modifying this Readme.md file accordingly. 

---

## Prerequisites

Before you begin, ensure you have the following installed on your system:

- **Docker**: [Install Docker](https://docs.docker.com/get-docker/)
- **Docker Compose** (optional, but recommended): [Install Docker Compose](https://docs.docker.com/compose/install/)

---

## Setting Up PostgreSQL with Docker

### 1. **Pull the PostgreSQL Docker Image**
   Download the official PostgreSQL Docker image with the following command:

   ```bash
   docker pull postgres:latest
   ```

### 2. **Create a Docker Volume**
   Create a Docker volume to persist PostgreSQL data:

   ```bash
   docker volume create postgres_data
   ```

   This volume will ensure data persistence, even if the container is removed.

### 3. **Run the PostgreSQL Container**
   Start the PostgreSQL container using the following command:

   ```bash
   docker run --name postgres -e POSTGRES_PASSWORD=your_password -d -p 5432:5432 -v postgres_data:/var/lib/postgresql/data postgres
   ```

   Replace `your_password` with a secure password for the PostgreSQL superuser (`postgres`).

   - The `-v postgres_data:/var/lib/postgresql/data` flag mounts the `postgres_data` volume to the container's data directory, ensuring data persistence.

### 4. **Verify the Container**
   To confirm the container is running, use:

   ```bash
   docker ps
   ```

   You should see the `postgres` container listed.

---

## Setting Up pgAdmin with Docker

### 1. **Pull the pgAdmin Docker Image**
   Download the official PostgreSQL Docker image with the following command:

   ```bash
   docker pull dpage/pgadmin4:latest
   ```

### 2. **Run the pgAdmin Container**
   Start the pgAdmin container using the following command:

   ```bash
   docker run --name pgadmin -d -p 5050:80 -e PGADMIN_DEFAULT_EMAIL=admin@example.com -e PGADMIN_DEFAULT_PASSWORD=admin dpage/pgadmin4:latest
   ```

   Replace `5050` with your desired port, and `admin@example.com` and `admin` with your preferred email and password for pgAdmin.

   - The `-p 5050:80` flag maps port `5050` on your host machine to port `80` inside the container (where pgAdmin runs).

### 3. **Access pgAdmin**
   Open your browser and go to:

   ```
   http://localhost:5050
   ```

   Log in using the email and password you set.

---

## Accessing PostgreSQL via pgAdmin

finding Host address: 
  ```bash
  docker inspect --format='{{.NetworkSettings.IPAddress}}' postgres
  ```

### 1. **Connect to the PostgreSQL Database**
   - After logging into pgAdmin, click on **Add New Server**.
   - In the **General** tab, provide a name for your server (e.g., `PostgreSQL Docker`).
   - In the **Connection** tab, enter the following details:
     - **Host name/address**: `postgres` (or the name of your PostgreSQL container). [usually  172.17.0.2 on windows]
     - **Port**: `5432` (default PostgreSQL port).
     - **Maintenance database**: `postgres` (default database).
     - **Username**: `postgres` (default superuser).
     - **Password**: The password you set for the PostgreSQL container (e.g., `your_password`).
   - Click **Save** to connect.

### 2. **Explore and Manage the Database**
   - Once connected, you can:
     - Create and manage databases.
     - Run SQL queries using the **Query Tool**.
     - View and edit tables, views, and stored procedures.
     - Monitor database activity and performance.

---

## Workshop Outcomes

By the end of this workshop, you will:

- Understand how to set up PostgreSQL and pgAdmin using Docker.
- Learn how to use Docker volumes to persist database data.
- Gain hands-on experience with basic and advanced database operations.

----
<a name="workshop-id"></a>
## 📝 Workshop Files & Scripts (to be modified by the students) 🧑‍🎓 

This workshop introduces key database concepts and provides hands-on practice in a controlled, containerized environment using PostgreSQL within Docker.

### Key Concepts Covered:

1. **Entity-Relationship Diagram (ERD)**:
   - Designed an ERD to model relationships and entities for the database structure.
   - Focused on normalizing the database and ensuring scalability.

   **[Add ERD Snapshot Here]**

   images/erd/ERD.PNG
   > ![ERD_image](images/erd/ERD.PNG)

    images/erd/DSD.png
   > ![ERD_image](images/erd/DSD.png)
   
 images/erd/addimagetoreadme.PNG  
> ![add_image_to readme_with_relative_path](images/erd/addimagetoreadme.PNG)

images/erd/one.jpg
> ![add_image_one.png](images/erd/one.jpg)

  
   *(Upload or link to the ERD image or file)*

3. **Creating Tables**:
   - Translated the ERD into actual tables, defining columns, data types, primary keys, and foreign keys.
   - Utilized SQL commands for table creation.

   **[Add Table Creation Code Here]**
   *(Provide or link to the SQL code used to create the tables)*


     code/sql/createtable.sql
   [Create_Table_Code](code/sql/createtable.sql)

   ## Database Schema Documentation

### 1. Customer Table
**Purpose**: The Customer table serves as the central entity in our banking/financial system, storing core personal information about each customer.

**Why we added it**: This is the primary entity that all other tables reference. Without customers, there would be no need for addresses, contacts, documents, etc.

**Attributes and their purposes**:
- `CustomerID (INT PRIMARY KEY)`: Unique identifier for each customer. We use an integer primary key for fast indexing and efficient joins with other tables.
- `Customer_First_Name (VARCHAR(50))`: Stores the customer's first name. 50 characters is sufficient for most names while preventing excessive storage use.
- `Customer_Last_Name (VARCHAR(50))`: Stores the customer's last name separately for better querying capabilities (e.g., searching by last name).
- `ssn (VARCHAR(20) UNIQUE)`: Social Security Number for unique identification. Made UNIQUE to prevent duplicate customers. VARCHAR(20) allows for formatting with dashes.
- `date_of_birth (DATE)`: Essential for age verification, legal compliance, and demographic analysis.
- `customer_since (DATE)`: Tracks customer relationship duration, useful for loyalty programs and customer segmentation.

### 2. Address Table
**Purpose**: Stores multiple addresses for each customer (home, work, vacation, etc.).

**Why we added it**: Customers often have multiple addresses, and separating this into its own table follows database normalization principles (avoiding data redundancy).

**Attributes and their purposes**:
- `addressID (INT PRIMARY KEY)`: Unique identifier for each address record.
- `customer_id (INT, FOREIGN KEY)`: Links the address to a specific customer. ON DELETE CASCADE ensures addresses are removed when a customer is deleted.
- `street_address (VARCHAR(255))`: Stores the street portion of the address. 255 characters accommodates long addresses.
- `city_name (VARCHAR(50))`: City information for geographic segmentation and correspondence.
- `state (VARCHAR(50))`: State/province information. 50 characters allows for full state names or international provinces.
- `zip_code (VARCHAR(20))`: Postal code as VARCHAR to handle international formats (some include letters).
- `country (VARCHAR(50))`: Country information for international customers.
- `asress_type (VARCHAR(50))`: Type of address (HOME, WORK, VACATION, etc.). Note: This appears to be a typo for "address_type".
- `is_primary (BOOLEAN)`: Flags the main address for correspondence and default shipping.

### 3. Contact Table
**Purpose**: Manages multiple contact methods for each customer (email, phone, fax, etc.).

**Why we added it**: Customers have various contact methods, and this design allows unlimited contact entries per customer while maintaining data integrity.

**Attributes and their purposes**:
- `contactID (INT PRIMARY KEY)`: Unique identifier for each contact record.
- `customer_id (INT, FOREIGN KEY)`: Links contact to customer with CASCADE deletion.
- `contact_type (VARCHAR(50))`: Categorizes contact method (EMAIL, PHONE, FAX, etc.).
- `contact_value (VARCHAR(100))`: The actual contact information. 100 characters accommodates email addresses and international phone numbers.
- `is_primary (BOOLEAN)`: Identifies the preferred contact method.

### 4. CustomerDocument Table
**Purpose**: Tracks important identification and verification documents for regulatory compliance.

**Why we added it**: Financial institutions must verify customer identity (KYC - Know Your Customer) and maintain records of identification documents.

**Attributes and their purposes**:
- `document_id (INT PRIMARY KEY)`: Unique identifier for each document.
- `customer_id (INT, FOREIGN KEY)`: Links document to customer.
- `document_type (VARCHAR(50))`: Type of document (PASSPORT, DRIVERS_LICENSE, etc.).
- `document_number (VARCHAR(50) UNIQUE)`: Document's official number. UNIQUE prevents duplicate document entries.
- `issue_date (DATE)`: When the document was issued.
- `expiry_date (DATE)`: Document expiration for compliance tracking.
- `verification_status (BOOLEAN)`: Whether the document has been verified by staff.
- `file_reference (VARCHAR(255))`: Path or reference to the scanned document file.

### 5. CustomerNote Table
**Purpose**: Records important interactions, observations, and customer service notes.

**Why we added it**: Maintains a history of customer interactions, complaints, and important information for customer service continuity.

**Attributes and their purposes**:
- `note_id (INT PRIMARY KEY)`: Unique identifier for each note.
- `customer_id (INT, FOREIGN KEY)`: Links note to customer.
- `employee_id (INT)`: Tracks which employee created the note (references an employee table not shown).
- `note_date (DATE)`: When the note was created.
- `note_category (VARCHAR(50))`: Categorizes notes (COMPLAINT, INQUIRY, ACCOUNT_REVIEW, etc.).
- `note_text (TEXT)`: The actual note content. TEXT type allows for lengthy notes.
- `is_important (BOOLEAN)`: Flags critical notes for immediate attention.

### 6. CustomerSegment Table
**Purpose**: Defines customer tiers or segments based on business rules.

**Why we added it**: Enables customer classification for targeted marketing, service levels, and benefits.

**Attributes and their purposes**:
- `segment_id (INT PRIMARY KEY)`: Unique identifier for each segment.
- `segment_name (VARCHAR(100))`: Name of the segment (STANDARD, PREMIUM, GOLD, PLATINUM).
- `description (TEXT)`: Detailed description of segment benefits and criteria.
- `min_balance_required (DECIMAL(10,2))`: Minimum account balance to qualify for this segment. DECIMAL ensures accurate financial calculations.

### 7. CustomerSegmentAssignment Table
**Purpose**: Associates customers with their current segment(s).

**Why we added it**: This junction table enables many-to-many relationships between customers and segments, allowing segment changes over time.

**Attributes and their purposes**:
- `assignment_id (INT PRIMARY KEY)`: Unique identifier for each assignment.
- `customer_id (INT, FOREIGN KEY)`: Links to the customer being assigned.
- `segment_id (INT, FOREIGN KEY)`: Links to the segment being assigned.
- `assigned_date (DATE)`: When the customer was assigned to this segment, enabling historical tracking.

## Key Design Decisions

1. **Normalization**: The schema follows third normal form (3NF) to minimize data redundancy and ensure data integrity.

2. **CASCADE Deletion**: All foreign keys use ON DELETE CASCADE to maintain referential integrity when customers are removed.

3. **Primary Keys**: All tables use integer primary keys for efficient indexing and joins.

4. **Data Types**: 
   - VARCHAR lengths are chosen based on expected data sizes
   - DECIMAL for financial values to avoid floating-point precision issues
   - BOOLEAN for binary states (is_primary, verification_status)
   - TEXT for unlimited-length content (notes, descriptions)

5. **Unique Constraints**: Applied to SSN and document numbers to prevent duplicates.

6. **Separate Tables**: Each major concept (addresses, contacts, documents) has its own table to support multiple entries per customer and maintain clean data organization.

3. **Generating Sample Data**:
   - Generated sample data to simulate real-world scenarios using **SQL Insert Statements**.
   - Used scripts to automate bulk data insertion for large datasets.

   **[Add Sample Data Insert Script Here]**
   *(Upload or link to the sample data insert scripts)*

   
   Backups/Backup1/excelTemplateGen.py
   [Excel_Gen_Code](Backups/Backup1%20/excelTemplateGen.py)


   Backups/Backup1/generatedata.py
   [Generate_Data_Python_Code](Backups/Backup1%20/generatedata.py)

   Backups/Backup1/generatedata.sql
   [Generate_Data_SQL_Code](Backups/Backup1%20/generatedata.sql)


   > ![Populated_Tables](images/erd/populated_tables.jpg)
   > ![insert_works](images/erd/insert_works.jpg)


   

5. **Writing SQL Queries**:
   - Practiced writing **SELECT**, **JOIN**, **GROUP BY**, and **ORDER BY** queries.
   - Learned best practices for querying data efficiently, including indexing and optimization techniques.
  
     part2/Constraints.sql
     [Constraints](part2/Constraints.sql)

     part2/Queries.sql
     [Queries](part2/Queries.sql)

     part2/RollBackCommit
     [RollBack](part2/RollBackCommit)

   **[Add Example SQL Query Here]**
   *(Provide or link to example SQL queries)*

6. **Stored Procedures and Functions**:
   - Created reusable **stored procedures** and **functions** to handle common database tasks.
   - Used SQL to manage repetitive operations and improve performance.

   **[Add Stored Procedures/Function Code Here]**
   *(Upload or link to SQL code for stored procedures and functions)*

7. **Views**:
   - Created **views** to simplify complex queries and provide data abstraction.
   - Focused on security by limiting user access to certain columns or rows.

   **[Add View Code Here]**
   *(Provide or link to the SQL code for views)*

8. **PostgreSQL with Docker**:
   - Set up a Docker container to run **PostgreSQL**.
   - Configured database connections and managed data persistence within the containerized environment.

   **[Add Docker Configuration Code Here]**
   *(Link to or provide the Docker run command and any configuration files)*

---

## 💡 Workshop Outcomes

By the end of this workshop, you should be able to:

- Design and create a database schema based on an ERD.
- Perform CRUD (Create, Read, Update, Delete) operations with SQL.
- Write complex queries using joins, aggregations, and subqueries.
- Create and use stored functions and procedures for automation and performance.
- Work effectively with PostgreSQL inside a Docker container for development and testing.

---

## Additional Tasks for Students

### 1. **Database Backup and Restore**
   - Use `pg_dump` to back up your database and `pg_restore` or `psql` to restore it.

   ```bash
   # Backup the database
   pg_dump -U postgres -d your_database_name -f backup.sql

   # Restore the database
   psql -U postgres -d your_database_name -f backup.sql
   ```

### 2. **Indexing and Query Optimization**
   - Create indexes on frequently queried columns and analyze query performance.

   ```sql
   -- Create an index
   CREATE INDEX idx_your_column ON your_table(your_column);

   -- Analyze query performance
   EXPLAIN ANALYZE SELECT * FROM your_table WHERE your_column = 'value';
   ```

### 3. **User Roles and Permissions**
   - Create user roles and assign permissions to database objects.

   ```sql
   -- Create a user role
   CREATE ROLE read_only WITH LOGIN PASSWORD 'password';

   -- Grant read-only access to a table
   GRANT SELECT ON your_table TO read_only;
   ```

### 4. **Advanced SQL Queries**
   - Write advanced SQL queries using window functions, recursive queries, and CTEs.

   ```sql
   -- Example: Using a window function
   SELECT id, name, salary, ROW_NUMBER() OVER (ORDER BY salary DESC) AS rank
   FROM employees;
   ```

### 6. **Database Monitoring**
   - Use PostgreSQL's built-in tools to monitor database performance.

   ```sql
   -- View active queries
   SELECT * FROM pg_stat_activity;

   -- Analyze table statistics
   SELECT * FROM pg_stat_user_tables;
   ```

### 7. **Using Extensions**
   - Install and use PostgreSQL extensions like `pgcrypto` or `postgis`.

   ```sql
   -- Install the pgcrypto extension
   CREATE EXTENSION pgcrypto;

   -- Example: Encrypt data
   INSERT INTO users (username, password) VALUES ('alice', crypt('password', gen_salt('bf')));
   ```

### 8. **Automating Tasks with Cron Jobs**
   - Automate database maintenance tasks (e.g., backups) using cron jobs.

   ```bash
   # Example: Schedule a daily backup at 2 AM
   0 2 * * * pg_dump -U postgres -d your_database_name -f /backups/backup_$(date +\%F).sql
   ```

### 9. **Database Testing**
   - Write unit tests for your database using `pgTAP`.

   ```sql
   -- Example: Test if a table exists
   SELECT * FROM tap.plan(1);
   SELECT tap.has_table('public', 'your_table', 'Table should exist');
   SELECT * FROM tap.finish();
   ```

---

## Troubleshooting

### 1. **Connection Issues**
   - **Problem**: Unable to connect to the PostgreSQL or pgAdmin container.
   - **Solution**:  
     - Ensure both the PostgreSQL and pgAdmin containers are running. You can check their status by running:
       ```bash
       docker ps
       ```
     - Verify that you have the correct container names. If you are unsure of the names, you can list all containers (running and stopped) with:
       ```bash
       docker ps -a
       ```
     - Ensure that the correct ports are mapped (e.g., `5432:5432` for PostgreSQL and `5050:80` for pgAdmin).
     - Verify that the `postgres` container's name is used in pgAdmin's connection settings.
     - If using `localhost` and experiencing connection issues, try using the container name instead (e.g., `postgres`).
     - Check the logs for any error messages:
       ```bash
       docker logs postgres
       docker logs pgadmin
       ```
     - If you are still having trouble, try restarting the containers:
       ```bash
       docker restart postgres
       docker restart pgadmin
       ```

### 2. **Forgot Password**
   - **Problem**: You've forgotten the password for pgAdmin or PostgreSQL.
   - **Solution**:
     - For pgAdmin:
       1. Stop the pgAdmin container:
          ```bash
          docker stop pgadmin
          ```
       2. Restart the container with a new password:
          ```bash
          docker run --name pgadmin -d -p 5050:80 -e PGADMIN_DEFAULT_EMAIL=admin@example.com -e PGADMIN_DEFAULT_PASSWORD=new_password dpage/pgadmin4:latest
          ```
     - For PostgreSQL:
       1. If you've forgotten the `POSTGRES_PASSWORD` for PostgreSQL, you’ll need to reset it. First, stop the container:
          ```bash
          docker stop postgres
          ```
       2. Restart it with a new password:
          ```bash
          docker run --name postgres -e POSTGRES_PASSWORD=new_password -d -p 5432:5432 -v postgres_data:/var/lib/postgresql/data postgres
          ```

### 3. **Port Conflicts**
   - **Problem**: Port is already in use on the host machine (e.g., port 5432 or 5050).
   - **Solution**:  
     - If a port conflict occurs (for example, PostgreSQL's default port `5432` is already in use), you can map a different host port to the container's port by changing the `-p` flag:
       ```bash
       docker run --name postgres -e POSTGRES_PASSWORD=your_password -d -p 5433:5432 -v postgres_data:/var/lib/postgresql/data postgres
       ```
       This would map PostgreSQL’s internal `5432` to the host’s `5433` port.
     - Similarly, for pgAdmin, you can use a different port:
       ```bash
       docker run --name pgadmin -d -p 5051:80 -e PGADMIN_DEFAULT_EMAIL=admin@example.com -e PGADMIN_DEFAULT_PASSWORD=admin dpage/pgadmin4:latest
       ```

### 4. **Unable to Access pgAdmin in Browser**
   - **Problem**: You cannot access pgAdmin through `http://localhost:5050` (or other port you have set).
   - **Solution**:
     - Ensure the pgAdmin container is running:
       ```bash
       docker ps
       ```
     - Double-check that the port mapping is correct and no firewall is blocking the port.
     - If using a non-default port (e.g., `5051` instead of `5050`), ensure you access it by visiting `http://localhost:5051` instead.

### 5. **Data Persistence Issue**
   - **Problem**: After stopping or removing the PostgreSQL container, the data is lost.
   - **Solution**:
     - Ensure that you are using a Docker volume for data persistence. When starting the container, use the `-v` flag to map the volume:
       ```bash
       docker run --name postgres -e POSTGRES_PASSWORD=your_password -d -p 5432:5432 -v postgres_data:/var/lib/postgresql/data postgres
       ```
     - To inspect or back up the volume:
       ```bash
       docker volume inspect postgres_data
       ```

### 6. **Accessing pgAdmin with Docker Network**
   - **Problem**: If you are trying to connect from pgAdmin to PostgreSQL and the connection is unsuccessful.
   - **Solution**:
     - Make sure both containers (PostgreSQL and pgAdmin) are on the same Docker network:
       ```bash
       docker network create pg_network
       docker run --name postgres --network pg_network -e POSTGRES_PASSWORD=your_password -d -p 5432:5432 -v postgres_data:/var/lib/postgresql/data postgres
       docker run --name pgadmin --network pg_network -d -p 5050:80 -e PGADMIN_DEFAULT_EMAIL=admin@example.com -e PGADMIN_DEFAULT_PASSWORD=admin dpage/pgadmin4:latest
       ```
     - This ensures that both containers can communicate over the internal network created by Docker.

---

# Queries

### 1. **Query to show all customers who have valid docs**
   > ![Valid Docs](images/queries/valid_docs.jpg)

### 2. **Query to show addresses of everyone who joined this year**
   > ![Current_Year](images/queries/current_year.jpg)

### 3. **Query to show all customers who sent in an important report or complaint**
   > ![Important_Report_Or_Complaint](images/queries/important_report_or_complaint.jpg)

### 4. **Query to show average customer age for each segment**
   > ![Average_Age_Per_Segment](images/queries/avg_age_per_segment.jpg)

### 5. **Query to show all customers whose documents expired more than a year ago**
   > ![Expired_Over_Year_ago](images/queries/expired_over_year_ago.jpg)

### 6. **Query to show how many customers signed up in each month**
   > ![Signed_Up_Per_Month](images/queries/signed_up_per_month.jpg)

### 7. **Query to show all customers who live in Longmen**
   > ![Live_In_Longmen](images/queries/live_in_longmen.jpg)

### 8. **Query to show primary contact info sorted by type**
   > ![Primary_Contact_Info](images/queries/primary_contact.jpg)


---

# Deletions

### 1. **Remove customers who haven't been updated in over 3 years and have expired documents**
   #### Before:
   > ![Before_Not_Updated_For_3_Years_Removal](images/queries/before_3_years.jpg)
   #### After:
   > ![After_Not_Updated_For_3_Years_Removal](images/queries/after_3_years.jpg)

### 2. **Remove contact records that are duplicates and not marked as primary**
   #### Before:
   > ![Before_Non_Primary_Duplicate_Contact_Records_Removal](images/queries/before_duplicates.jpg)
   #### After:
   > ![After_Non_Primary_Duplicate_Contact_Records_Removal](images/queries/after_duplicates.jpg)

### 3. **Remove all non-primary addresses that are outside of China**
   #### Before:
   > ![Before_Non_Primary_And_Non_Chinese_Removal](images/queries/before_china.jpg)
   #### After:
   > ![Before_Non_Primary_And_Non_Chinese_Removal](images/queries/after_china.jpg)

# Updates

### 1. **Update all notes of customers over 65 to important**
   #### Before:
   > ![Before_Updated_Notes_For_Over_65](images/queries/before_65.jpg)
   #### After:
   > ![After_Updated_Notes_For_Over_65](images/queries/after_65.jpg)

### 2. **Update all expired documents to be unverified**
   #### Before:
   > ![Before_Expired_Docs_Marked_Unverified](images/queries/before_expired.jpg)
   #### After:
   > ![After_Expired_Docs_Marked_Unverified](images/queries/after_expired.jpg)

### 3. **Promote all customers whose documents are valid and verified and of type img/gif**
   #### Before:
   > ![Before_Verified_Img/Gif_Promoted_Part_1](images/queries/before_promotion1.jpg)
   > ![Before_Verified_Img/Gif_Promoted_Part_2](images/queries/before_promotion2.jpg)
   #### After:
   > ![After_Verified_Img/Gif_Promoted](images/queries/after_promotion.jpg)

# Rollback

   #### Mid Rollback:
   > ![Mid_Rollback](images/queries/before_rollback.jpg)
   #### After Rollback:
   > ![After_Rollback](images/queries/after_rollback.jpg)

# Commit
   #### Before:
   > ![Before_Commit](images/queries/before_commit.jpg)
   #### After:
   > ![After_Commit](images/queries/after_commit.jpg)

# Constraints
### 1. **All customers date of birth has to be before today**
   > ![Date_of_birth_must_be_before_today](images/queries/dob_before_today.jpg)

### 2. **Sets default address to home if none provided**
   > ![Set_Default_Address_As_Home](images/queries/default_address.jpg)

### 3. **Ensure every contact has not null email or phone**
   > ![Not_Null_Email_Or_Phone](images/queries/not_null_contact_info.jpg)


---
## Integration

### Their stuff
#### Their DSD
> ![Their_DSD](images/theirs/their_dsd.jpg)

#### Their ERD
> ![Their_DSD](images/theirs/their_erd.jpg)


### Integrated stuff

#### Design Decisions

Here's a short explanation of the ERD design decisions:

**One-to-Many Relationships (Most Common):**
- **Employee → Customer**: One employee manages multiple customers (realistic business scenario)
- **Customer → Address/Contact/Documents**: Customers need multiple addresses (home, work), contact methods (phone, email), and documents (ID, passport)
- **Employee → Position**: Employees have job history - current and past positions
- **Department → Employee**: One department contains many employees (organizational hierarchy)

**Many-to-One Relationships:**
- **Employee → Department**: Multiple employees belong to one department (reporting structure)
- **Customer → Employee**: Multiple customers assigned to one employee (workload distribution)

**One-to-One Relationship:**
- **Department → Manager**: Each department has exactly one manager (clear accountability)

**Many-to-Many Relationship:**
- **Customer ↔ Segment**: Customers can belong to multiple segments over time (VIP, Premium, etc.), and segments contain multiple customers. Used junction table CustomerSegmentAssignment to track when assignments happened.

**Why This Design:**
- Reflects real business relationships (employees manage customers, departments have hierarchies)
- Prevents data redundancy (separate tables for addresses vs. storing in customer table)
- Maintains data integrity with proper foreign keys
- Supports historical tracking (position history, segment changes over time)

The design follows normalization principles while keeping it practical for a customer-employee management system.


#### Integrated DSD
> ![Integrated_DSD](images/integrated/integrated_dsd.jpg)

#### Integrated ERD
> ![Integrated_ERD](images/integrated/integrated_erd.jpg)

---


## 👇 Resources

- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [pgAdmin Documentation](https://www.pgadmin.org/docs/)
- [Docker Documentation](https://docs.docker.com/)

