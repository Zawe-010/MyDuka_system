# Importing flask to use it
from flask import Flask , render_template

# Instantiate your application - initialization of Flask
# A flask instance
app = Flask(__name__)

# __name__ - is a special built in variable
# It represents the name of the current file where your application is built
# It tells Flask where your project starts

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/products')
def products():
    return "My Products"

@app.route('/sales')
def sales():
    return "My Sales"

# Running your application
app.run(debug=True)