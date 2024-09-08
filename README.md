README: Sales Data Analysis and MySQL Operations

Overview
This Python script connects to a MySQL database named ecommerce_sales, loads sales data from a CSV file, and performs various SQL operations on the data, including creating and populating tables, updating data, and querying the database. The script demonstrates proficiency in SQL and Python by utilizing a variety of SQL features such as JOIN, GROUP BY, Temporary Tables, and Common Table Expressions (CTEs).

Features
Create and Insert Data: Automatically creates and populates Orders, Products, and OrderDetails tables using data from the CSV file.
Date and Time Handling: Handles date and time extraction from a single timestamp column in the dataset and inserts it into two separate columns: order_date and order_time.
SQL Queries: Demonstrates various SQL operations including data insertion, updates, joins, and ordering.
Temporary Tables and CTEs: Includes examples of using a temporary table and a common table expression (CTE) to perform advanced queries.
Table Descriptions
Orders:

order_id (INT, Primary Key)
order_date (DATE)
order_time (TIME)
city (VARCHAR)
purchase_address (VARCHAR)
Products:

product_id (INT, AUTO_INCREMENT, Primary Key)
product_category (VARCHAR)
product_name (VARCHAR)
price_each (DECIMAL)
OrderDetails:

order_id (INT, Foreign Key to Orders)
product_id (INT, Foreign Key to Products)
quantity_ordered (INT)
sales (DECIMAL)
SQL Queries in the Script
1. Insert Data into Tables
Data from the CSV is inserted into Orders, Products, and OrderDetails tables using basic INSERT statements with ON DUPLICATE KEY UPDATE to avoid duplicates.
2. Date and Time Handling
Dates and times are extracted from a datetime string, split into separate columns (order_date and order_time), and inserted into the Orders table.
3. Advanced Queries
Total Sales by Product: Displays the total sales amount for each product.

sql
Copy code
SELECT product_name, SUM(sales) AS total_sales
FROM OrderDetails
JOIN Products ON OrderDetails.product_id = Products.product_id
GROUP BY product_name;
Total Sales by City: Shows the total sales for each city.

sql
Copy code
SELECT city, SUM(sales) AS total_sales
FROM Orders
JOIN OrderDetails ON Orders.order_id = OrderDetails.order_id
GROUP BY city;
Advanced SQL Techniques
Common Table Expression (CTE)
Find the Most Popular Products:
This query uses a CTE to calculate the total quantity ordered for each product and then displays the top 5 most ordered products.
python
Copy code
cursor.execute(
    """
    WITH ProductSales AS (
        SELECT product_name, SUM(quantity_ordered) AS total_quantity
        FROM OrderDetails
        JOIN Products ON OrderDetails.product_id = Products.product_id
        GROUP BY product_name
    )
    SELECT product_name, total_quantity
    FROM ProductSales
    ORDER BY total_quantity DESC
    LIMIT 5;
    """
)
result = cursor.fetchall()
print("CTE Example - Top 5 Most Ordered Products:")
for row in result:
    print(row)
Temporary Table
Find Top 5 Cities by Total Sales:
This query creates a temporary table that calculates total sales by city, then retrieves the top 5 cities with the highest total sales.
python
Copy code
cursor.execute(
    """
    CREATE TEMPORARY TABLE TempCitySales AS
    SELECT city, SUM(sales) AS total_sales
    FROM Orders
    JOIN OrderDetails ON Orders.order_id = OrderDetails.order_id
    GROUP BY city;
    """
)
db.commit()

cursor.execute(
    """
    SELECT city, total_sales
    FROM TempCitySales
    ORDER BY total_sales DESC
    LIMIT 5;
    """
)
result = cursor.fetchall()
print("Temporary Table Example - Top 5 Cities by Total Sales:")
for row in result:
    print(row)

# Clean up: Drop the temporary table
cursor.execute("DROP TEMPORARY TABLE IF EXISTS TempCitySales;")
Requirements
Python 3.x
MySQL Database
pandas: For reading CSV and data manipulation
mysql-connector-python: For connecting Python to MySQL
You can install the required packages using:

bash
Copy code
pip install pandas mysql-connector-python
Instructions
Database Setup: Ensure you have a MySQL server running with a database named ecommerce_sales.
CSV File: The script expects a CSV file with columns such as Order ID, Order Date, City, Purchase Address, Product, Quantity Ordered, and Sales. Update the file path in the script to match your local CSV file path.
Run the Script: Execute the Python script to load data into the MySQL database, run the queries, and display results.
