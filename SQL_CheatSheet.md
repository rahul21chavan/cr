# SQL & Database Concepts Cheat Sheet

This guide covers foundational and advanced SQL and relational database topics, with practical syntax for SQL Server and PostgreSQL. It is designed for learning, quick reference, and interview prep.

---

## 1. What is SQL and a Database?

- **SQL (Structured Query Language):** The standard language for querying and manipulating relational databases.
- **Database:** A structured collection of data (tables, schemas) offering ACID transactions, indexing, and concurrency control.

---

## 2. RDBMS

- **Relational Database Management System:** Stores data in tables (rows/columns) with relationships using Primary Keys (PK) and Foreign Keys (FK).
- **Examples:** SQL Server, PostgreSQL, MySQL, Oracle.

---

## 3. Types of SQL Commands

- **DDL:** Data Definition Language (CREATE, ALTER, DROP, TRUNCATE)
- **DML:** Data Manipulation Language (INSERT, UPDATE, DELETE, MERGE)
- **DQL:** Data Query Language (SELECT)
- **DCL:** Data Control Language (GRANT, REVOKE)
- **TCL:** Transaction Control Language (COMMIT, ROLLBACK, SAVEPOINT)

---

## 4. Creating a Database

- **SQL Server:**  
  `CREATE DATABASE mydb;`
- **PostgreSQL:**  
  `CREATE DATABASE mydb;`
- Consider collation, encoding, owners, file locations for enterprise use.

---

## 5. Components of an RDBMS

- **Parser, Optimizer, Executor, Storage Engine, Transaction Manager, Buffer/Cache, Access Control**
- Understanding these helps in performance tuning and troubleshooting.

---

## 6. What is an SQL Query?

- A statement to request data or perform actions.
- Structure:  
  `SELECT <columns> FROM <tables> [JOINs] [WHERE] [GROUP BY] [HAVING] [ORDER BY] [LIMIT]`

---

## 7. SQL Clauses

- **SELECT, FROM, JOIN, WHERE, GROUP BY, HAVING, ORDER BY, LIMIT/TOP, WITH (CTE)**

---

## 8–15. Examples of Basic SQL Clauses

- **SELECT & FROM:**  
  `SELECT col1, col2 FROM table;`
- **WHERE:**  
  `WHERE col = 'value' AND col2 > 5`
- **ORDER BY:**  
  `ORDER BY last_name ASC, created_at DESC`
- **GROUP BY / HAVING:**  
  `GROUP BY dept HAVING COUNT(*) > 5`
- **DISTINCT:**  
  `SELECT DISTINCT country FROM customers;`
- **TOP / LIMIT:**  
  `SELECT TOP 10 * FROM table;` (SQL Server)  
  `SELECT * FROM table LIMIT 10;` (Postgres)

---

## 16. Query Execution Order

Logical order:  
`FROM → JOIN → WHERE → GROUP BY → HAVING → SELECT → ORDER BY → LIMIT`

---

## 17–20. Defining & Modifying Schema

- **CREATE TABLE (SQL Server):**
  ```sql
  CREATE TABLE dbo.employees (
    emp_id INT IDENTITY(1,1) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    hire_date DATE
  );
  ```
- **CREATE TABLE (Postgres):**
  ```sql
  CREATE TABLE employees (
    emp_id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    hire_date DATE
  );
  ```
- **ALTER TABLE:**  
  `ALTER TABLE table ADD COLUMN col INT;`
- **DROP TABLE:**  
  `DROP TABLE IF EXISTS schema.table;`

---

## 21–24. Core DML Statements

- **INSERT:**  
  `INSERT INTO t(col1, col2) VALUES (v1, v2);`
- **UPDATE:**  
  `UPDATE t SET col = new WHERE condition;`
- **DELETE:**  
  `DELETE FROM t WHERE condition;`
- **TRUNCATE:**  
  `TRUNCATE TABLE t;` (fast, but not always rollbackable)

---

## 25–30. Filtering & Search

- **Comparison:** `=, <>, !=, <, >, <=, >=`
- **Logical:** `AND, OR, NOT`
- **BETWEEN:**  
  `col BETWEEN 10 AND 20`
- **IN/NOT IN:**  
  `col IN (a, b, c)`  
  Beware `NOT IN` with NULLs.
- **LIKE / ILIKE (Postgres):**  
  `LIKE 'abc%'` or `ILIKE 'abc%'` (case-insensitive)
- **Regex:**  
  Postgres: `~`, `~*`, `SIMILAR TO`

---

## 31–41. Joins

- **INNER JOIN:**  
  Returns matching rows in both tables.
- **LEFT JOIN:**  
  All rows from left, matching from right or NULL.
- **RIGHT JOIN:**  
  All rows from right, matching from left.
- **FULL OUTER JOIN:**  
  All rows from both tables.
- **SELF JOIN:**  
  Join table to itself via aliases.
- **CROSS JOIN:**  
  Cartesian product.
- **ANTI JOIN:**  
  Rows in one table not in another (see examples below).

---

## 42–47. Set Operators

- **UNION:** Removes duplicates
- **UNION ALL:** Keeps duplicates (faster)
- **INTERSECT:** Rows in both queries
- **EXCEPT:** Rows in A not in B

---

## 48–70. Functions (Scalar, Aggregate, String, Numeric, Date/Time)

- **Scalar:** `UPPER()`, `SUBSTRING()`, `ROUND()`
- **Aggregate:** `SUM()`, `AVG()`, `COUNT()`
- **String:** `CONCAT()`, `LOWER()`, `TRIM()`, `REPLACE()`, `LEN()`, `LEFT()`, `RIGHT()`, `SUBSTRING()`
- **Numeric:** `ROUND()`, `CEIL()`, `FLOOR()`, `ABS()`, `MOD()`
- **Date/Time:** `NOW()`, `CURRENT_DATE`, `EXTRACT()`, `DATEADD()`, `DATEDIFF()`, `EOMONTH()`, `TO_CHAR()`

---

## 71–97. Handling Types, NULLs, and Conditionals

- **Validation:** Constraints, TRY_CAST, safe conversion
- **ISDATE:** SQL Server only
- **COALESCE vs ISNULL:** COALESCE is ANSI, ISNULL is T-SQL.
- **NULLIF:** Returns NULL if two values are equal.
- **CASE WHEN:** Conditional logic in queries.

---

## 98–109. Advanced Window Functions

- **Window Aggregates:**  
  `SUM(col) OVER (PARTITION BY p ORDER BY o)`
- **Ranking:**  
  `RANK()`, `DENSE_RANK()`, `ROW_NUMBER()`
- **NTILE:**  
  `NTILE(4) OVER (ORDER BY score DESC)`
- **FIRST_VALUE, LAST_VALUE:**  
  Returns values from window frames.

---

## 110–112. Analytical Window Functions

- **LEAD/LAG:** Access next/previous row's value.
- **FIRST_VALUE/LAST_VALUE:** With window frames.

---

## 113–117. Subqueries and CTEs

- **Subqueries:** Used in `SELECT`, `WHERE`, `FROM`.
- **CTE (WITH):** Improves readability, can be recursive for hierarchical data.

---

## 118–120. Views & Temp Tables

- **CREATE VIEW v AS ...**
- **Materialized Views (Postgres):** Stores result set.
- **Temp Tables:**  
  - SQL Server: `CREATE TABLE #temp (...)`
  - Postgres: `CREATE TEMP TABLE temp (...)`

---

## 121–126. Constraints

- **NOT NULL, UNIQUE, PRIMARY KEY, FOREIGN KEY, CHECK, DEFAULT**

---

## 127–128. Grouping Extensions & Stored Procedures

- **ROLLUP & CUBE:** For hierarchical/multidimensional aggregates.
- **Stored Procedures:** Reusable routines (syntax varies by DB).

---

## 129–130. Exception Handling and Indexes

- **Exception Handling:**  
  - SQL Server: `TRY...CATCH`
  - Postgres: `BEGIN...EXCEPTION WHEN...THEN...END;`
- **Indexes:** B-tree, composite, unique, covering. Use `EXPLAIN` to analyze usage.

---

## 131–132. Project Ideas

- **Exploratory Data Analysis (EDA):** Analyze e‑commerce dataset (schema design, cleansing, cohort analysis, dashboards).
- **Advanced Analytics:** Analytics pipeline (ETL, window functions, feature engineering, star-schema, automation). Use both SQL Server and Postgres for comparison.

---

## Practical Example Queries

### Top-N per group (ROW_NUMBER)
```sql
WITH ranked AS (
  SELECT user_id, score,
         ROW_NUMBER() OVER (PARTITION BY region ORDER BY score DESC) rn
  FROM leaderboard
)
SELECT * FROM ranked WHERE rn <= 3;
```

### Anti-join safe with NULLs
```sql
SELECT a.*
FROM A a
WHERE NOT EXISTS (SELECT 1 FROM B b WHERE b.key = a.key);
```

### Running total (window sum)
```sql
SELECT order_date, amount,
       SUM(amount) OVER (ORDER BY order_date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) running_total
FROM orders;
```

### Recursive CTE (employee hierarchy)
```sql
WITH RECURSIVE mgrs AS (
  SELECT emp_id, manager_id, name FROM employees WHERE manager_id IS NULL
  UNION ALL
  SELECT e.emp_id, e.manager_id, e.name
  FROM employees e
  JOIN mgrs m ON e.manager_id = m.emp_id
)
SELECT * FROM mgrs;
```

---

## Best Practices & Tips

- Prefer explicit `JOIN ... ON` syntax.
- Always use `WHERE` for UPDATE/DELETE; wrap in transaction for safety.
- Use `EXPLAIN`/`EXPLAIN ANALYZE` to inspect query plans.
- Use appropriate data types, avoid `SELECT *` in production.
- Index for read patterns; remove unused indexes.
- Normalize to avoid redundancy; denormalize for analytic workloads as needed.
- Be cautious with NULL handling and string-vs-null differences.
- Use `COPY` / bulk-load utilities for large datasets.

---

**For more advanced project ideas and SQL deep dives, see sections 131–132.**
