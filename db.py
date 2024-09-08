import mysql.connector
import pandas as pd

# Connect to MySql
db = mysql.connector.connect(
    host="localhost", user="root", password="mysqlpassword", database="ecommerce_sales"
)

cursor = db.cursor()

print("MySql database connection successful!")

# Load the CSV file into a DataFrame
data = pd.read_csv(r"C:\Users\Bibek Paudel\Desktop\Data Science\Sales Data Analysis.csv")

# Convert 'Order Date' to datetime
data["Order DateTime"] = pd.to_datetime(data["Order Date"], format="%d-%m-%Y %H:%M")

# Split into separate date and time columns
data["Order Date"] = data["Order DateTime"].dt.strftime("%Y-%m-%d")
data["Order Time"] = data["Order DateTime"].dt.strftime("%H:%M:%S")

# Populate Orders table
for _, row in data.iterrows():
    cursor.execute(
        """
        INSERT INTO Orders (order_id, order_date, city, purchase_address)
        VALUES (%s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE order_date = %s, city = %s, purchase_address = %s;
    """,
        (
            row["Order ID"],
            row["Order Date"],
            row["City"],
            row["Purchase Address"],
            row["Order Date"],
            row["City"],
            row["Purchase Address"],
        ),
    )

# Insert data into Products table
unique_products = data[["Product Category", "Product", "Price Each"]].drop_duplicates()
for _, row in unique_products.iterrows():
    cursor.execute(
        """
        INSERT INTO Products (product_category, product_name, price_each)
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE price_each=%s;
    """,
        (row["Product Category"], row["Product"], row["Price Each"], row["Price Each"]),
    )

# Insert data into OrderDetails table
for _, row in data.iterrows():
    cursor.execute(
        """
        INSERT INTO OrderDetails (order_id, product_id, quantity_ordered, sales)
        SELECT %s, product_id, %s, %s
        FROM Products
        WHERE product_name = %s
        ON DUPLICATE KEY UPDATE quantity_ordered=%s, sales=%s;
    """,
        (
            row["Order ID"],
            row["Quantity Ordered"],
            row["Sales"],
            row["Product"],
            row["Quantity Ordered"],
            row["Sales"],
        ),
    )

db.commit()
print("Data inserted successfully!")

# Populate Order time with the time
for _, row in data.iterrows():
    cursor.execute(
        """
        UPDATE Orders
        SET order_time = %s
        WHERE order_id = %s
    """,
        (row["Order Time"], row["Order ID"]),
    )

db.commit()
print("Order time updated successfully!")

# Remove the time from order_date column
cursor.execute(
    """
    ALTER TABLE Orders MODIFY order_date DATE;
"""
)
db.commit()
print("order_date column modified successfully!")

# Query 1: Count Orders per City
cursor.execute(
    """
    SELECT city, COUNT(order_id) AS num_orders
    FROM Orders
    GROUP BY city
    ORDER BY num_orders DESC;
"""
)
result = cursor.fetchall()
print("\nOrders per City:")
for row in result:
    print(row)

# Query 2: Find Total Sales by Product
cursor.execute(
    """
    SELECT p.product_name, SUM(od.sales) AS total_sales
    FROM OrderDetails od
    JOIN Products p ON od.product_id = p.product_id
    GROUP BY p.product_name
    ORDER BY total_sales DESC;
"""
)
result = cursor.fetchall()
print("\nTotal Sales by Product:")
for row in result:
    print(row)

# Query 3: Find Top Selling Products (by quantity)
cursor.execute(
    """
    SELECT p.product_name, SUM(od.quantity_ordered) AS total_quantity
    FROM OrderDetails od
    JOIN Products p ON od.product_id = p.product_id
    GROUP BY p.product_name
    ORDER BY total_quantity DESC;
"""
)
result = cursor.fetchall()
print("\nTop Selling Products (by quantity):")
for row in result:
    print(row)

# Query 4: Get Total Revenue per City
cursor.execute(
    """
    SELECT o.city, SUM(od.sales) AS total_revenue
    FROM Orders o
    JOIN OrderDetails od ON o.order_id = od.order_id
    GROUP BY o.city
    ORDER BY total_revenue DESC;
"""
)
result = cursor.fetchall()
print("\nTotal Revenue per City:")
for row in result:
    print(row)

# Query 5: Retrieve Orders within a Date Range
start_date = "2019-01-01"
end_date = "2019-12-31"
cursor.execute(
    """
    SELECT order_id, order_date, city
    FROM Orders
    WHERE order_date BETWEEN %s AND %s
    ORDER BY order_date;
""",
    (start_date, end_date),
)
result = cursor.fetchall()
print(f"\nOrders between {start_date} and {end_date}:")
for row in result:
    print(row)

# Query 6: Average Sales per Order
cursor.execute(
    """
    SELECT o.order_id, AVG(od.sales) AS avg_sales
    FROM Orders o
    JOIN OrderDetails od ON o.order_id = od.order_id
    GROUP BY o.order_id;
"""
)
result = cursor.fetchall()
print("\nAverage Sales per Order:")
for row in result:
    print(row)

# Query 7: Products Never Sold
cursor.execute(
    """
    SELECT product_name
    FROM Products p
    LEFT JOIN OrderDetails od ON p.product_id = od.product_id
    WHERE od.product_id IS NULL;
"""
)
result = cursor.fetchall()
print("\nProducts Never Sold:")
for row in result:
    print(row)

# Query 8: Orders with Multiple Products
cursor.execute(
    """
    SELECT order_id, COUNT(product_id) AS num_products
    FROM OrderDetails
    GROUP BY order_id
    HAVING num_products > 1;
"""
)
result = cursor.fetchall()
print("\nOrders with Multiple Products:")
for row in result:
    print(row)

# Query 9: Cities with Highest Revenue
cursor.execute(
    """
    SELECT o.city, SUM(od.sales) AS total_revenue
    FROM Orders o
    JOIN OrderDetails od ON o.order_id = od.order_id
    GROUP BY o.city
    ORDER BY total_revenue DESC;
"""
)
result = cursor.fetchall()
print("\nCities with Highest Revenue:")
for row in result:
    print(row)

# Query 10: Most Popular Product Category
cursor.execute(
    """
    SELECT p.product_category, SUM(od.quantity_ordered) AS total_quantity
    FROM Products p
    JOIN OrderDetails od ON p.product_id = od.product_id
    GROUP BY p.product_category
    ORDER BY total_quantity DESC;
"""
)
result = cursor.fetchall()
print("\nMost Popular Product Category:")
for row in result:
    print(row)

# Query 11: Total Quantity Ordered by Product Category
cursor.execute(
    """
    SELECT p.product_category, SUM(od.quantity_ordered) AS total_quantity
    FROM Products p
    JOIN OrderDetails od ON p.product_id = od.product_id
    GROUP BY p.product_category;
"""
)
result = cursor.fetchall()
print("\nTotal Quantity Ordered by Product Category:")
for row in result:
    print(row)

# Query 12: Find Customers with the Most Orders
cursor.execute(
    """
    SELECT city, COUNT(order_id) AS num_orders
    FROM Orders
    GROUP BY city
    ORDER BY num_orders DESC
    LIMIT 5;
"""
)
result = cursor.fetchall()
print("\nCities with the Most Orders:")
for row in result:
    print(row)

# Close the connection
cursor.close()
db.close()