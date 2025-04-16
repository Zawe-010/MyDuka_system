import psycopg2

# Create a connection to db
conn = psycopg2.connect(user="postgres", password="Zawadi@2006#",host="localhost",port="5432",database="myduka")

# Executes database operations
cur = conn.cursor()

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

# Calling the functions back
fetch_products()
fetch_sales()




