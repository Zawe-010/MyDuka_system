# Importing flask to use it
from flask import Flask , render_template, request, redirect, url_for
from database import fetch_products,fetch_sales,insert_products,insert_sales, profit_per_product, profit_per_day, sales_per_product, sales_per_day


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
    
@app.route('/sales')
def sales():
    sales = fetch_sales()
    products = fetch_products()
    return render_template("sales.html", sales = sales, products = products)

@app.route('/make_sales', methods=['POST'])
def make_sales():
    if request.method == 'POST' : 
        product_id= request.form['p-id']
        quantity = request.form['quantity']
        new_sale = (product_id, quantity)
        insert_sales(new_sale)
        return redirect(url_for('sales'))
    
@app.route('/dashboard')
def dashboard():
    profit_product = profit_per_product()
    sales_product = sales_per_product()
    profit_day = profit_per_day()
    sales_day = sales_per_day()

    # List Comprehension
    product_name = [i[0] for i in profit_product]
    p_profit = [float(i[1]) for i in profit_product]
    p_sales = [float(i[1]) for i in sales_product]

     # Day Metrics-data
    date = [str(i[0]) for i in profit_day]
    p_day = [float(i[1]) for i in profit_day]
    s_day = [float(i[1]) for i in sales_day]
    return render_template("dashboard.html",
                           product_name = product_name, p_profit = p_profit, p_sales = p_sales,
                           date = date, p_day = p_day, s_day = s_day)


# Running your application
app.run(debug=True)
