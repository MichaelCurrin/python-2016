/* I picked up a few short handy commands which I want to share with others
I tested them on MySQLWorkbench*/

-- ####################
-- count rows in table
-- ####################

SELECT COUNT(*) FROM tbl_company


SELECT SUM(TABLE_ROWS) 
FROM INFORMATION_SCHEMA.TABLES 
WHERE TABLE_SCHEMA = 'db_cipla_test3';


-- ####################
-- selecting a database
-- ####################

-- double-click on db name to select as default
-- OR "USE"
USE db_connectors_cipla;
SELECT COUNT(*) from information_schema.tables
WHERE table_type = 'base table'


-- ####################
-- Get Columns
-- ####################

-- get distinct list of columns
SELECT DISTINCT (COLUMN_NAME)
    FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_SCHEMA='db_connectors_cipla'
    ORDER BY COLUMN_NAME;
    

-- ####################
-- Count rows in tables
-- ####################

-- show number of rows in each table for a DB

SELECT TABLE_SCHEMA, TABLE_NAME, TABLE_ROWS 
FROM INFORMATION_SCHEMA.TABLES 
WHERE  TABLE_SCHEMA LIKE 'db_cipla_test_' and TABLE_ROWS > 0 
ORDER BY `TABLES`.`TABLE_NAME` ASC, `TABLES`.`TABLE_SCHEMA`  ASC

-- ####################
-- show variables
-- ####################

SHOW SESSION variables

--

-- Databases
SHOW databases;

-- Users and host
SELECT user,host FROM mysql.user;

-- Grants
SHOW GRANTS;
GRANT ALL PRIVILEDGES ON *.* TO 'root'@'localhost' WITH GRANT OPTION
GRANT PROX ON "@" TO 'root'@'localhost' WITH GRANT OPTION


-- ####################
-- Get date range
-- ####################

-- Show the first and last dates in a table's timestamp column

SELECT 
MIN(timestamp) AS 'Earliest date',
MAX(timestamp) AS 'Latest date'	
FROM tbl_socialposts; 


