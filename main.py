# Importing flask to use it
from flask import Flask , render_template, request, redirect, url_for
from database import fetch_products,fetch_sales,insert_products,insert_sales


# Instantiate your application - initialization of Flask
# A flask instance
app = Flask(__name__)

# __name__ - is a special built in variable
# It represents the name of the current file where your application is built
# It tells Flask where your project starts

@app.route('/')
def home():
    numbers = [1,2,3,4,5]
    return render_template("index.html", numbers = numbers)

@app.route('/products')
def products():
    products = fetch_products()
    return render_template("products.html", products = products)

@app.route('/add_products', methods=['POST'])
def add_products():
    if request.method == 'POST' : 
        name = request.form['p-name']
        buying_price = request.form['b-price']
        selling_price = request.form['s-price']
        stock_quantity =request.form['quantity']
        new_product = (name, buying_price, selling_price, stock_quantity)
        insert_products(new_product)
        return redirect(url_for('products'))
    

@app.route('/add_sales', methods=['POST'])
def add_sales():
    if request.method == 'POST' : 
        pid= request.form['p-id']
        quantity = request.form['quantity']
        created_at = request.form['created_at']
        new_sale = (pid, quantity, created_at )
        insert_sales(new_sale)
        return redirect(url_for('sales'))

@app.route('/sales')
def sales():
    sales = fetch_sales()
    return render_template("sales.html", sales = sales)

@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")

# Running your application
app.run(debug=True)
