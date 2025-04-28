# Importing flask to use it
from flask import Flask , render_template
from database import fetch_products,fetch_sales


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

@app.route('/sales')
def sales():
    sales = fetch_sales()
    return render_template("sales.html", sales = sales)

# Running your application
app.run(debug=True)
