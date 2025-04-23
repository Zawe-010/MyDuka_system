# Importing flask to use it
from flask import Flask 

# Instantiate your application - initialization of Flask
# A flask instance
app = Flask(__name__)

# __name__ - is a special built in variable
# It represents the name of the current file where your application is built
# It tells Flask where your project starts

@app.route('/products')
def home():
    return "My Home Page"

# Running your application
app.run()