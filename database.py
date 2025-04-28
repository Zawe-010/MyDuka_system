import psycopg2
from datetime import datetime

# Create a connection to db
conn = psycopg2.connect(user="postgres", password="Zawadi@2006#",host="localhost",port="5432",database="myduka")

# Executes database operations
cur = conn.cursor()

current_datetime = datetime.now()
print("This is the time and date now: ",current_datetime)

# Query
def fetch_products():
    cur.execute("SELECT * FROM products;")

    products = cur.fetchall()
    return products

# Fetching sales
def fetch_sales():
    cur.execute("SELECT * FROM sales;")

    sales = cur.fetchall()
    return sales

# A query inserting a product
def insert_product():
    cur.execute("INSERT INTO products(name,buying_price,selling_price,stock_quantity) VALUES('Milk',50,60,100);")
    # Saving operations
    conn.commit()
    return "Products Inserted"
# A query inserting a sale
def insert_sale():
    cur.execute(f"INSERT INTO sales(pid,quantity,created_at) VALUES(3,15,'{current_datetime}');")
    # Saving operations
    conn.commit()
    return "Sales made"

product = insert_product()
sale = insert_sale()
print(sale)
print(product)


fetch_products()
fetch_sales()

# Task(for fetch)

def fetch_data(table):
    cur.execute(f"SELECT * FROM {table};")
    data = cur.fetchall()
    return data

# products = fetch_data('products')
# sales = fetch_data('sales')
# print("Products from fetch data func:\n",products)
# print("Sales from fetch data func:\n",sales)

# Task(for insert)
# Method 1(takes values as parameters)
def insert_products(values):
    # Use of placeholders
    insert = "INSERT INTO products(name, buying_price, selling_price, stock_quantity) VALUES(%s,%s,%s,%s)"
    cur.execute(insert, values)
    conn.commit()

product_values = ("Meat", 120, 150, 200)
insert_products(product_values)
products = fetch_data('products')
print("Fetching data after modified func.\n",products)

def insert_sales(values):
    insert_2 = "INSERT INTO sales(pid, quantity, created_at) VALUES(%s, %s, %s)"
    cur.execute(insert_2, values)
    conn.commit()

# Fix datetime string formatting
sales_values = (4, 20, current_datetime)
insert_sales(sales_values)
sales = fetch_data('sales')
print("Fetching data after modified func.\n",sales)

# Method 2 (take values as parameter but doesn't use placeholders).
# Instead we replace placeholders with {values} parameter in a formatted string.
# def insert_products_method(values):
#     insert = f"INSERT INTO products(name, buying_price, selling_price, stock_quantity) VALUES{values}"
#     cur.execute(insert)
#     conn.commit()

# product_values = (" Mango",40,50,100)
# insert_products_method(product_values)
# products = fetch_data('products')
# print("Fetching prods method:\n",products)

# def insert_products_method(values):
#     insert = f"INSERT INTO sales(pid, quantity, created_at) VALUES{values}"
#     cur.execute(insert)
#     conn.commit()

# sales_values_values = (10,25, current_datetime)
# insert_products_method(sales_values)
# sales = fetch_data('sales')
# print("Fetching prods method:\n",sales)

# Method 3 - Insert data into multiple tables with varying number of columns
# Insert  into <table_name>(columns)values()
# def insert_data(table,columns,values):
#     cur.execute(f"INSERT INTO{table} ({columns}) values{values}")
#     conn.commit()

# table = 'products'
# columns = "name, buying_price, selling_price, stock_quantity"
# values = ("Phone", 8000,12000,10)

# table_2 = 'sales'
# columns = "pid, quantity, created_at"
# sales_values = (12,3,current_datetime)
# insert_data(table, columns,values)

# products = fetch_data('products')
# print("Data from last method:\n",products)

