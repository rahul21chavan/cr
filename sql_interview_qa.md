# SQL Interview Questions & Answers (With Examples)

---

## 1. SQL Basics

### **Q1. Difference between WHERE and HAVING?**
- `WHERE` filters rows **before** grouping/aggregation (on raw data).
- `HAVING` filters rows **after** aggregation (on grouped data).

**Example:**
```sql
SELECT city, COUNT(*) 
FROM customers
WHERE country = 'India'      -- filters before count
GROUP BY city
HAVING COUNT(*) > 10;        -- filters after count
```

---

### **Q2. Difference between DELETE, TRUNCATE, and DROP?**
| Operation | Removes Data | Removes Structure | Rollback Possible | Resets Identity? | Speed       |
|-----------|--------------|------------------|-------------------|------------------|-------------|
| DELETE    | Yes (rows)   | No               | Yes               | No               | Slower      |
| TRUNCATE  | Yes (all)    | No               | No (sometimes)    | Yes              | Fast        |
| DROP      | Yes (all)    | Yes (table)      | No                | N/A              | Fastest     |

---

### **Q3. Difference between INNER JOIN and LEFT JOIN?**
- `INNER JOIN`: Returns only matching rows from both tables.
- `LEFT JOIN`: Returns all rows from the left table, with matching rows from the right (or NULLs if no match).

**Example:**
```sql
SELECT a.*, b.*
FROM A a
INNER JOIN B b ON a.id = b.a_id;   -- Only matched rows

SELECT a.*, b.*
FROM A a
LEFT JOIN B b ON a.id = b.a_id;    -- All rows from A, matched (or NULL) from B
```

---

### **Q4. How do you remove duplicate rows from a table?**
```sql
-- Keep one, remove others
DELETE FROM my_table
WHERE id NOT IN (
    SELECT MIN(id)
    FROM my_table
    GROUP BY col1, col2, col3
);
```
Or use `ROW_NUMBER()` in modern SQL:
```sql
WITH cte AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY col1, col2, col3 ORDER BY id) AS rn
  FROM my_table
)
DELETE FROM cte WHERE rn > 1;
```

---

### **Q5. Difference between UNION and UNION ALL?**
- `UNION`: Combines results, removes duplicates.
- `UNION ALL`: Combines results, keeps all duplicates.

---

### **Q6. What is a primary key vs a foreign key?**
- **Primary Key**: Uniquely identifies each row in a table. Cannot be NULL.
- **Foreign Key**: Column(s) that refer to the primary key in another table, creating a relationship.

---

## 2. Aggregate Functions

### **Q1. What are aggregate functions? Give examples.**
- Functions that operate on sets of rows and return a single value.
- Examples: `SUM()`, `COUNT()`, `AVG()`, `MAX()`, `MIN()`

---

### **Q2. How to count unique values in a column?**
```sql
SELECT COUNT(DISTINCT column_name) FROM table_name;
```

---

### **Q3. How do you calculate the percentage of total per group?**
```sql
SELECT region,
       SUM(sales) AS total_sales,
       100.0 * SUM(sales) / SUM(SUM(sales)) OVER () AS pct_of_total
FROM sales
GROUP BY region;
```

---

### **Q4. How to calculate cumulative total using SQL?**
```sql
SELECT date,
       sales,
       SUM(sales) OVER (ORDER BY date) AS cum_sales
FROM daily_sales;
```

---

## 3. Grouping and Filtering

### **Q1. How does GROUP BY work?**
- Groups rows sharing one or more column values.
- Aggregate functions are applied to each group.

**Example:**
```sql
SELECT department, COUNT(*) FROM employees GROUP BY department;
```

---

### **Q2. Can you use WHERE with GROUP BY? What about HAVING?**
- `WHERE`: Used **before** GROUP BY, filters raw rows.
- `HAVING`: Used **after** GROUP BY, filters groups.

---

### **Q3. Find the total sales per region, filter those above 1M.**
```sql
SELECT region, SUM(sales) AS total_sales
FROM sales
GROUP BY region
HAVING SUM(sales) > 1000000;
```

---

## 4. SQL Joins 🔥

### **Q1. Difference between INNER, LEFT, RIGHT, FULL joins?**
| Join Type   | Rows Returned                                      |
|-------------|----------------------------------------------------|
| INNER JOIN  | Only rows with matches in both tables              |
| LEFT JOIN   | All rows from left + matching rows from right      |
| RIGHT JOIN  | All rows from right + matching rows from left      |
| FULL JOIN   | All rows from both, matched or unmatched           |

---

### **Q2. Query: customers who didn’t place any order**
```sql
SELECT c.*
FROM customers c
LEFT JOIN orders o ON c.id = o.customer_id
WHERE o.id IS NULL;
```

---

### **Q3. What is a self join and when is it used?**
- A join of a table with itself.
- Used for comparing rows within the same table (e.g., employee hierarchy).

**Example:**
```sql
SELECT a.name AS emp, b.name AS manager
FROM employees a
LEFT JOIN employees b ON a.manager_id = b.id;
```

---

### **Q4. What is a cross join and its use case?**
- Returns Cartesian product (all combinations).
- Use case: generating all possible pairs, calendar dates, etc.

**Example:**
```sql
SELECT * FROM products CROSS JOIN stores;
```

---

### **Q5. Difference between semi join and anti join?**
- **Semi Join**: Returns rows from the left table that have a match in the right (but doesn’t return right table columns).
- **Anti Join**: Returns rows from the left table that **do not** have a match in the right.

In SQL, anti-join uses `LEFT JOIN ... WHERE right.id IS NULL`.

---

## 5. Window Functions 🔥🔥

### **Q1. What are window functions in SQL?**
- Functions that perform calculations across a set of rows related to the current row, without collapsing them.  
- Examples: `ROW_NUMBER()`, `RANK()`, `SUM() OVER (...)`

---

### **Q2. Difference between RANK, DENSE_RANK, and ROW_NUMBER?**
| Function      | Gaps in Rank? | Ties get same rank? | Example result |
|---------------|---------------|---------------------|---------------|
| RANK()        | Yes           | Yes                 | 1,1,3         |
| DENSE_RANK()  | No            | Yes                 | 1,1,2         |
| ROW_NUMBER()  | No            | No                  | 1,2,3         |

---

### **Q3. Find top 3 salaries per department**
```sql
SELECT *
FROM (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC) AS rn
  FROM employees
) t
WHERE rn <= 3;
```

---

### **Q4. Use case of LAG() and LEAD() functions**
- `LAG()`: Accesses previous row’s value
- `LEAD()`: Accesses next row’s value

**Example:**
```sql
SELECT date, sales,
       LAG(sales) OVER (ORDER BY date) AS prev_day_sales
FROM daily_sales;
```

---

### **Q5. What is PARTITION BY and ORDER BY in windows?**
- `PARTITION BY`: Splits data into groups (like GROUP BY but doesn’t collapse rows)
- `ORDER BY`: Sets sort order within partition for calculations

---

## 6. Subqueries & CTEs

### **Q1. What is a subquery? Difference between correlated and non-correlated subquery?**
- **Subquery**: Query inside another query
- **Non-correlated**: Can run independently
- **Correlated**: Depends on outer query's rows

**Example:**
```sql
-- Non-correlated
SELECT name FROM employees WHERE dept_id = (SELECT id FROM departments WHERE name='HR');

-- Correlated
SELECT name FROM employees e WHERE salary > (SELECT AVG(salary) FROM employees WHERE dept_id = e.dept_id);
```

---

### **Q2. What is a Common Table Expression (CTE)? Syntax and use cases?**
- A temporary named result set, used for readability and reuse.

**Syntax:**
```sql
WITH cte_name AS (
  SELECT ... FROM ...
)
SELECT * FROM cte_name;
```
**Use cases:** Recursion, chaining logic, breaking complex queries

---

### **Q3. Query: second highest salary using subquery**
```sql
SELECT MAX(salary) FROM employees WHERE salary < (SELECT MAX(salary) FROM employees);
```

---

### **Q4. Query: running total of daily sales using CTE**
```sql
WITH sales_cte AS (
  SELECT date, sales,
         SUM(sales) OVER (ORDER BY date) AS running_total
  FROM daily_sales
)
SELECT * FROM sales_cte;
```

---

## 7. String & Date Functions

### **Q1. How do you extract year/month from a date?**
```sql
SELECT EXTRACT(YEAR FROM order_date) AS year,
       EXTRACT(MONTH FROM order_date) AS month
FROM orders;
```
Or vendor-specific:  
`YEAR(order_date)`, `MONTH(order_date)`

---

### **Q2. Convert a string to uppercase and remove spaces.**
```sql
SELECT UPPER(REPLACE(name, ' ', '')) FROM employees;
```

---

### **Q3. Difference between CHARINDEX, SUBSTRING, and LEFT/RIGHT**
- `CHARINDEX` (or `INSTR`): Finds the position of a substring
- `SUBSTRING`: Extracts part of a string from a position
- `LEFT/RIGHT`: Gets the leftmost/rightmost N characters

---

### **Q4. Get the difference in days between two date columns.**
```sql
SELECT DATEDIFF(day, start_date, end_date) FROM events;
-- Or: end_date - start_date (Postgres)
```

---

## 8. Advanced SQL – Real-world Scenarios

### **Q1. Query: find duplicate rows in a table**
```sql
SELECT col1, col2, COUNT(*)
FROM my_table
GROUP BY col1, col2
HAVING COUNT(*) > 1;
```

---

### **Q2. Get the latest transaction for each customer**
```sql
SELECT *
FROM (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY trans_date DESC) AS rn
  FROM transactions
) t
WHERE rn = 1;
```

---

### **Q3. Query to pivot rows into columns**
*(Example: Sales by month)*
```sql
SELECT customer_id,
  SUM(CASE WHEN month='Jan' THEN sales ELSE 0 END) AS Jan,
  SUM(CASE WHEN month='Feb' THEN sales ELSE 0 END) AS Feb
FROM sales
GROUP BY customer_id;
```

---

### **Q4. Find customers who placed orders every month in 2024**
```sql
SELECT customer_id
FROM orders
WHERE YEAR(order_date) = 2024
GROUP BY customer_id
HAVING COUNT(DISTINCT MONTH(order_date)) = 12;
```

---

### **Q5. Sessions where login and logout span > 1 hour**
```sql
SELECT *
FROM log_table
WHERE TIMESTAMPDIFF(hour, login_time, logout_time) > 1;
```

---

## 9. Optimization + Performance

### **Q1. How do indexes help performance?**
- Enable faster searches by letting DBMS quickly locate data without scanning all rows.

---

### **Q2. Difference between clustered and non-clustered indexes?**
- **Clustered**: Physically reorders the table; only one per table (usually primary key)
- **Non-clustered**: Separate structure with pointers to data; many per table.

---

### **Q3. How to optimize a slow-running SQL query?**
- Add indexes on search/join columns
- Select only needed columns
- Avoid functions on indexed columns in WHERE
- Use `EXPLAIN PLAN` to analyze
- Break complex queries into CTEs or temp tables

---

### **Q4. What is an EXPLAIN PLAN and how do you use it?**
- Shows how DBMS will execute a query (steps, indexes, joins)
- Used to diagnose bottlenecks

**Example:**
```sql
EXPLAIN SELECT * FROM orders WHERE customer_id = 123;
```

---

### **Q5. Difference between materialized view and normal view?**
- **View**: Stored query, runs each time accessed
- **Materialized view**: Stores actual data snapshot, updated periodically, faster for reads

---

## 10. Data Modeling + Constraints

### **Q1. What is normalization? 1NF, 2NF, 3NF?**
- **Normalization**: Organizing tables to reduce redundancy

| Form | Rule |
|------|------|
| 1NF  | Atomic (no repeating groups) |
| 2NF  | 1NF + all non-key columns fully depend on PK |
| 3NF  | 2NF + no transitive dependencies |

---

### **Q2. When would you denormalize a database?**
- For read-heavy analytics, performance, or reporting; to reduce joins at the cost of redundancy.

---

### **Q3. What are constraints in SQL?**
- **CHECK**: Restricts column values
- **DEFAULT**: Sets a default value
- **UNIQUE**: Enforces unique values
- **NOT NULL**: Disallows NULLs

---

### **Q4. Difference between OLTP and OLAP?**
- **OLTP**: Online Transaction Processing (frequent small updates, normalized)
- **OLAP**: Online Analytical Processing (complex queries, reporting, often denormalized)

---

## 11. Transactional SQL

### **Q1. What are ACID properties?**
- **Atomicity**: All or none
- **Consistency**: Valid state
- **Isolation**: Transactions don’t interfere
- **Durability**: Once committed, survives failures

---

### **Q2. Use of BEGIN, COMMIT, and ROLLBACK?**
- `BEGIN`: Starts transaction
- `COMMIT`: Saves changes
- `ROLLBACK`: Undoes changes since BEGIN

---

### **Q3. Difference between ISOLATION LEVELS: Read Committed vs Repeatable Read?**
- **Read Committed**: No dirty reads, but non-repeatable reads possible.
- **Repeatable Read**: No dirty or non-repeatable reads, but phantom reads possible.

---

## 12. Practice Coding Tasks (Hands-on)

### **Q1. Get the 2nd highest salary in each department.**
```sql
SELECT department, MAX(salary) AS second_highest
FROM employees
WHERE salary < (SELECT MAX(salary) FROM employees e2 WHERE e2.department = employees.department)
GROUP BY department;
```
Or using ROW_NUMBER:
```sql
SELECT department, salary
FROM (
  SELECT department, salary,
         ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC) rn
  FROM employees
) t
WHERE rn = 2;
```

---

### **Q2. Calculate 7-day rolling average sales.**
```sql
SELECT date, sales,
       AVG(sales) OVER (ORDER BY date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS rolling_avg
FROM daily_sales;
```

---

### **Q3. List all employees who have more than one manager**
```sql
SELECT employee_id
FROM employee_managers
GROUP BY employee_id
HAVING COUNT(DISTINCT manager_id) > 1;
```

---

### **Q4. Pivot sales by month columns from row format**
```sql
SELECT employee_id,
       SUM(CASE WHEN month='Jan' THEN sales ELSE 0 END) AS Jan,
       SUM(CASE WHEN month='Feb' THEN sales ELSE 0 END) AS Feb
FROM sales
GROUP BY employee_id;
```

---

### **Q5. Calculate retention: users who signed up in Jan and returned in Feb**
```sql
SELECT user_id
FROM users
WHERE signup_month = 'Jan'
AND user_id IN (
    SELECT user_id FROM logins WHERE login_month = 'Feb'
);
```

---

## 13. Bonus: SQL in ETL/Data Engineering Context

### **Q1. How do you validate source vs target row counts?**
```sql
SELECT COUNT(*) FROM source_table;
SELECT COUNT(*) FROM target_table;
-- Compare results to ensure all rows migrated
```

---

### **Q2. Write SQL to check schema drift between two tables**
```sql
SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name IN ('table1', 'table2')
GROUP BY column_name, data_type
HAVING COUNT(*) = 1;
```

---

### **Q3. How do you do SCD (slowly changing dimension) handling in SQL?**
- **Type 1**: Overwrite old data
- **Type 2**: Add new row with versioning and effective dates

**Example Type 2:**
```sql
-- Add new row if value changes
INSERT INTO dim_table (key, value, start_date, end_date)
SELECT key, new_value, CURRENT_DATE, NULL
FROM staging
WHERE key NOT IN (SELECT key FROM dim_table WHERE end_date IS NULL)
   OR value <> (SELECT value FROM dim_table WHERE key = staging.key AND end_date IS NULL);

-- Update end_date of old row
UPDATE dim_table
SET end_date = CURRENT_DATE
WHERE key IN (SELECT key FROM staging) AND end_date IS NULL AND value <> (SELECT value FROM staging WHERE key = dim_table.key);
```

---

### **Q4. Write SQL to check for data duplication or null key issues**
```sql
-- Duplicates
SELECT key_column, COUNT(*)
FROM my_table
GROUP BY key_column
HAVING COUNT(*) > 1;

-- Null keys
SELECT * FROM my_table WHERE key_column IS NULL;
```

---

**Tip:** Always clarify SQL dialect (MySQL, Postgres, SQL Server, etc.) as syntax may vary slightly.