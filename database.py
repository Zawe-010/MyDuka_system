import psycopg2
from datetime import datetime

# Create a connection to db
conn = psycopg2.connect(user="postgres", password="Zawadi@2006#",host="localhost",port="5432",database="myduka")

# Executes database operations
cur = conn.cursor()

current_datetime = datetime.now()


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

# Fetching sales
def fetch_stock():
    cur.execute("SELECT * FROM stock;")

    stock = cur.fetchall()
    return stock

# A query inserting a product
# def insert_product():
#     cur.execute("INSERT INTO products(name,buying_price,selling_price) VALUES('Milk',50,60);")
#     # Saving operations
#     conn.commit()
#     return "Products Inserted"
# # A query inserting a sale
# def insert_sale():
#     cur.execute(f"INSERT INTO sales(pid,quantity,created_at) VALUES(3,15,'{current_datetime}');")
#     # Saving operations
#     conn.commit()
#     return "Sales made"

# product = insert_product()
# sale = insert_sale()


# fetch_products()
# fetch_sales()

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
    insert = "INSERT INTO products(name, buying_price, selling_price) VALUES(%s,%s,%s)"
    cur.execute(insert, values)
    conn.commit()

# product_values = ("Meat", 120, 150)
# insert_products(product_values)
# products = fetch_data('products')


def insert_sales(values):
    insert_2 = "INSERT INTO sales(pid, quantity, created_at) VALUES(%s, %s, now())"
    cur.execute(insert_2, values)
    conn.commit()

# # Fix datetime string formatting
# sales_values = (4, 20, current_datetime)
# insert_sales(sales_values)
# sales = fetch_data('sales')

def insert_stock(values):
    insert_3 = "INSERT INTO stock(pid, stock_quantity, created_at) VALUES(%s, %s, now())"
    cur.execute(insert_3, values)
    conn.commit()


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

def profit_per_product():
    cur.execute("""
        SELECT products.name, 
               SUM((products.selling_price - products.buying_price) * sales.quantity) AS profit 
        FROM products 
        JOIN sales ON products.id = sales.pid 
        GROUP BY products.name;
    """)
    profit_per_product = cur.fetchall()
    return profit_per_product

# profit_product = profit_per_product()
# print(profit_product)

def profit_per_day():
    cur.execute("""
        SELECT DATE(sales.created_at) as date, 
               SUM((products.selling_price - products.buying_price) * sales.quantity) AS profit 
        FROM products 
        JOIN sales ON products.id = sales.pid 
        GROUP BY DATE(sales.created_at);
    """)
    profit_per_day = cur.fetchall()
    return profit_per_day

def sales_per_product():
    cur.execute("""
        SELECT products.name, 
               SUM(products.selling_price * sales.quantity) AS revenue
        FROM products 
        JOIN sales ON products.id = sales.pid 
        GROUP BY products.name;
    """)
    sales_per_product = cur.fetchall()
    return sales_per_product

def sales_per_day():
    cur.execute("""
        SELECT DATE(sales.created_at) as date, 
               SUM(products.selling_price * sales.quantity) AS revenue
        FROM sales 
        JOIN products ON products.id = sales.pid 
        GROUP BY DATE(sales.created_at);
    """)
    sales_per_day = cur.fetchall()
    return sales_per_day

def check_user(email):
    query = "SELECT * FROM users WHERE email = %s;"
    cur.execute(query,(email,))
    user = cur.fetchone()
    return user  

def insert_user(user_details):
    query = "insert into users(full_name,email,phone_number,password)values(%s,%s,%s,%s)"
    cur.execute(query,user_details)
    conn.commit()
    
def get_stock(pid):
     query = "select stock_quantity from stock where pid = %s"
     cur.execute(query,(pid,))
     stock = cur.fetchone()
     return stock


def available_stock(pid):
    cur.execute("select coalesce(sum(stock_quantity),0) from stock where pid = %s",(pid,))
    total_stock = cur.fetchone()[0] or 0
    cur.execute("select coalesce(sum(sales.quantity),0) from sales where pid = %s",(pid,))
    total_sold = cur.fetchone()[0] or 0
    return total_stock - total_sold

def product_name(pid):
    cur.execute("SELECT name FROM products WHERE id = %s", (pid,))
    product = cur.fetchone()[0] or "Unknown Prod"
    return product

def edit_product(values):
    cur.execute("update products set name = %s, buying_price = %s, selling_price = %s where id = %s", values)
    conn.commit()

def getnumberofproducts():
    cur.execute(" select * from products")
    products=cur.fetchall()
    no_products= len(products)
    return no_products

def getnumberofsales():
    cur.execute(" select * from sales")
    sales=cur.fetchall()
    no_sales= len(sales)
    return no_sales

def get_stock_count():
    cur.execute("SELECT COALESCE(SUM(stock_quantity), 0) FROM stock")
    total = cur.fetchone()[0]
    return total


def get_sales_today():
    today = datetime.now().date()
    cur.execute("""
        SELECT COALESCE(SUM(products.selling_price * sales.quantity), 0)
        FROM sales
        JOIN products ON sales.pid = products.id
        WHERE DATE(sales.created_at) = %s
    """, (today,))
    total_sales = cur.fetchone()[0]
    return total_sales


def get_sales_this_month():
    cur.execute("""
        SELECT COALESCE(SUM(products.selling_price * sales.quantity), 0)
        FROM sales
        JOIN products ON sales.pid = products.id
        WHERE EXTRACT(MONTH FROM sales.created_at) = EXTRACT(MONTH FROM CURRENT_DATE)
          AND EXTRACT(YEAR FROM sales.created_at) = EXTRACT(YEAR FROM CURRENT_DATE)
    """)
    total_sales = cur.fetchone()[0]
    return total_sales


def get_profit_today():
    today = datetime.now().date()
    cur.execute("""
        SELECT COALESCE(SUM((products.selling_price - products.buying_price) * sales.quantity), 0)
        FROM sales
        JOIN products ON sales.pid = products.id
        WHERE DATE(sales.created_at) = %s
    """, (today,))
    profit = cur.fetchone()[0]
    return profit


def get_profit_this_month():
    cur.execute("""
        SELECT COALESCE(SUM((products.selling_price - products.buying_price) * sales.quantity), 0)
        FROM sales
        JOIN products ON sales.pid = products.id
        WHERE EXTRACT(MONTH FROM sales.created_at) = EXTRACT(MONTH FROM CURRENT_DATE)
          AND EXTRACT(YEAR FROM sales.created_at) = EXTRACT(YEAR FROM CURRENT_DATE)
    """)
    profit = cur.fetchone()[0]
    return profit
