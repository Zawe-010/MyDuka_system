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

    print("Products:")
    for product in products:
        print(product)

# Fetching sales
def fetch_sales():
    cur.execute("SELECT * FROM sales;")

    sales = cur.fetchall()

    print("\nSales:")
    for sale in sales:
        print(sale)

# A query inserting a product
def insert_product():
    cur.execute("INSERT INTO products(name,buying_price,selling_price,stock_quantity) VALUES('Milk',50,60,100);")
    # Saving operations
    conn.commit()
    return "Products Inserted"
# # A query inserting a sale
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

