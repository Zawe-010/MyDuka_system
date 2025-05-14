# Importing flask to use it
from flask import Flask , render_template, request, redirect, url_for, flash, session
from database import fetch_products,fetch_sales,insert_products,insert_sales, profit_per_product, profit_per_day, sales_per_product, sales_per_day, check_user, insert_user, insert_stock, fetch_stock, available_stock
from flask_bcrypt import Bcrypt
from functools import wraps

# Instantiate your application - initialization of Flask
# A flask instance
app = Flask(__name__)

# A bycrypt instance
bcrypt = Bcrypt(app)

# __name__ - is a special built in variable
# It represents the name of the current file where your application is built
# It tells Flask where your project starts

@app.route('/')
def home():
    numbers = [1,2,3,4,5]
    return render_template("index.html", numbers = numbers)

def login_required(f):
    @wraps(f)
    def protected(*args,**kwargs):
        if 'email' not in session:
            return redirect(url_for('login'))
        return f(*args,**kwargs)
    return protected

@app.route('/products')
@login_required
def products():
    products = fetch_products()
    return render_template("products.html", products = products)

@app.route('/add_products', methods=['POST'])
def add_products():
    if request.method == 'POST' : 
        name = request.form['p-name']
        buying_price = request.form['b-price']
        selling_price = request.form['s-price']
        new_product = (name, buying_price, selling_price)
        insert_products(new_product)
        return redirect(url_for('products'))
    
@app.route('/sales')
@login_required
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
        stock_available = available_stock(product_id)
        if stock_available < float(quantity):
            flash("Insufficient stock","info")
        insert_sales(new_sale)
        flash("Sale made successfully","success")
        return redirect(url_for('sales'))

@app.route('/stock')
@login_required
def stock():
    products = fetch_products()
    stock = fetch_stock()
    return render_template('stock.html', products = products, stock = stock)

@app.route('/add_stock', methods = ['GET','POST'])
def add_stock():
      if request.method == 'POST' :
         product_id = request.form['p-id']
         stock_quantity = request.form['quantity']
         new_stock = (product_id,stock_quantity)
         insert_stock(new_stock)
         flash("Stock added successfully", "success")
         return redirect(url_for('stock'))

@app.route('/dashboard')
@login_required
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

@app.route('/register', methods = ['GET','POST'])
def register():
    if request.method == 'POST':
        full_name = request.form['full_name']
        email = request.form['email']
        phone_number = request.form['phone']
        password = request.form['password']

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        
        user = check_user(email)
        if not user:
            new_user = (full_name, email, phone_number, hashed_password)
            insert_user (new_user)
            return redirect(url_for('login'))
        else:
            print ("already registered")
    return render_template('register.html')

@app.route('/login', methods = ['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = check_user(email)
        if not user:
            flash('User not found,please register','danger')
            return redirect(url_for('register'))
        else:
            if bcrypt.check_password_hash(user[-1],password):
                flash('Logged in','success')
                session['email'] = email
                return redirect(url_for('dashboard'))
            else:
                flash('Password incorrect','danger')
    return render_template("login.html")

@app.route('/logout')
@login_required
def logout():
    session.pop('email', None)
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))

# Running your application
app.run(debug=True)
