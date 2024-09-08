
Project: E-Commerce Sales Data Integration and Analysis
Description:
This Python script connects to a MySQL database, creates necessary tables, inserts data from a CSV file, and executes various SQL queries to manage and analyze e-commerce sales data. It showcases proficiency in SQL by implementing key queries and handling data transformations like splitting date and time, and updating the database.

Database Tables:
Orders: Contains details of customer orders.

Columns: order_id, order_date, city, purchase_address, order_time.
Products: Contains information about products.

Columns: product_id, product_category, product_name, price_each.
OrderDetails: Contains details of each order.

Columns: order_id, product_id, quantity_ordered, sales.
Features:
CSV Parsing: Loads data from a CSV file into a Pandas DataFrame, processes date and time values, and prepares it for insertion into the MySQL database.
Data Insertion: Inserts new data into Orders, Products, and OrderDetails tables.
Data Update: Updates existing data in the Orders table to add time details.
Key SQL Queries:
Join Queries:
Fetch details of orders, products, and sales using JOIN.
Date and Time Operations:
Insert and update date and time details from the CSV file into the database.
Sales Analysis:
Retrieve total sales, count of orders, and average sales by product category, city, and other criteria.
Order Time Management:
Split order date and time for detailed time analysis.
SQL Proficiency Demonstrated:
Create Table statements for the main tables.
Insert and Update queries for data management.
JOIN queries to combine data from multiple tables.
Aggregate functions like SUM(), COUNT(), and AVG() for sales analysis.
Group By and Order By clauses for data grouping and sorting.
Handling ON DUPLICATE KEY UPDATE for efficient data updates.
How to Use:
Set Up the MySQL Database:

Ensure MySQL is installed and running on your local machine.
Update the connection credentials (host, user, password, database) in the script.
Create an ecommerce_sales database in MySQL.
Prepare the CSV File:

Update the file path to your CSV file containing the sales data.
Ensure the columns in the CSV match the script's data expectations (e.g., Order ID, Order Date, Product, etc.).
Run the Script:

The script will automatically create the tables (if not already present) and insert data into the database.
Run SQL Queries:

The script executes various SQL queries to demonstrate proficiency, including JOIN, GROUP BY, ORDER BY, and SUM() functions.
Modify the queries as needed to suit your specific analysis or project requirements.
Requirements:
Python Libraries:
mysql.connector for MySQL connection.
pandas for data handling and CSV reading.
MySQL Database:
MySQL server with an ecommerce_sales database.
Properly configured MySQL user credentials.
Additional Features:
Dynamic date and time handling using Python’s datetime module and Pandas.
Robust error handling for MySQL queries and data transformations.
Future Enhancements:
Expand the set of queries to include more complex analysis like customer segmentation, sales forecasting, or product recommendation.
Integrate data visualizations using libraries like Matplotlib or Seaborn.
Automate CSV file uploads for regular data updates.
