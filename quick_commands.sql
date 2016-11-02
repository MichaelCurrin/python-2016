/* I picked up a few short handy commands which I want to share with others
I tested them on MySQLWorkbench*/

-- ####################
-- count rows in table
-- ####################

SELECT COUNT(*) FROM tbl_company


-- ####################
-- selecting a database
-- ####################

-- double-click on db name to select as default
-- OR "USE"
USE db_yap_connectors_cipla;
SELECT COUNT(*) from information_schema.tables
WHERE table_type = 'base table'

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
-- GRANT ALL PRIVILEDGES ON *.* TO 'root'@'localhost' WITH GRANT OPTION
-- GRANT PROX ON "@" TO 'root'@'localhost' WITH GRANT OPTION
