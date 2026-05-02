from flask import Flask, request, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    date_joined = db.Column(db.DateTime)

    orders = db.relationship("Order", back_populates="user")# use the relationship function to create a relationship between the User and Order tables, this will allow us to access the orders associated with a user using user.orders and access the user associated with an order using order.user

# create an association table to represent the many-to-many relationship between orders and products, this table will have two foreign key columns that reference the primary keys of the Order and Product tables, and a composite primary key that consists of both foreign key columns
order_product = db.Table("order_product",
        db.Column("order_id", db.ForeignKey("order.id"), primary_key=True),
        db.Column("product_id", db.ForeignKey("product.id"), primary_key=True)
    )

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    total = db.Column(db.Integer)
    user_id = db.Column(db.ForeignKey("user.id"))# use the ForeignKey class to create a foreign key relationship between the Order and User tables, this will create a user_id column in the Order table that references the id column in the User table

    user = db.relationship("User", back_populates="orders")# use the relationship function to create a relationship between the Order and User tables, this will allow us to access the user associated with an order using order.user and access the orders associated with a user using user.orders
    products = db.relationship("Product", secondary=order_product, back_populates="orders")

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

    orders = db.relationship("Order", secondary=order_product, back_populates="products")

@app.route("/")
def index():
    return render_template("index.html", page_name="index", page_num=2)

@app.route("/home", methods=["GET"])
def home():
    return render_template("home.html", number=5, data=[{'key': 'value1'}, {'key': 'value2'}, {'key': 'value3'}])

@app.route("/json")
def json():
    return {"mykey": "JSON Value!", "mylist": [1, 2, 3, 4, 5]}

@app.route("/dynamic", defaults={"user_input": "default"})
@app.route("/dynamic/<user_input>")
def dynamic(user_input):
    return f"<h1>The user entered: {user_input}</h1>"

@app.route("/query")
def query():
    first = request.args.get("first")
    second = request.args.get("second")
    return f"<h1>The query string contains: {first} and {second}</h1>"

@app.route("/form", methods=["GET", "POST"])
def form():
    if request.method == "POST":
        user_input = request.form["user_input"]
        print(user_input)
        return redirect(url_for("home"))
        
    return '<form method="POST"><input type="text" name="user_input" /><input type="submit" /></form>'

@app.route("/acceptjson")
def acceptjson():
    json_data = request.get_json()
    api_input = json_data["mylist"]
    hello = json_data["hello"]
    return {"api_input": api_input, "hello": hello}

@app.route("/error")
def error():
    a = 1 / 0
    return "Error"

def insert_data():
    from datetime import datetime

    python_user = User(name="Python User", date_joined=datetime.now())
    flask_user = User(name="Flask User", date_joined=datetime.now())
    javascript_user = User(name="JavaScript User", date_joined=datetime.now())

    db.session.add_all([python_user, flask_user, javascript_user]) # use the session object to add the new users to the database, you can add multiple objects at once using the add_all method and passing a list of objects

    first_order = Order(total=99, user=python_user)# when creating a new order, we can set the user by passing the user object to the user parameter, this will automatically set the user_id foreign key column in the Order table to the id of the user
    second_order = Order(total=20, user=python_user)
    third_order = Order(total=199, user=flask_user)

    db.session.add_all([first_order, second_order, third_order])
    db.session.commit()

def update_first_user():
    user = User.query.first()
    user.name = "Flask User"

    db.session.commit()

def delete_first_user():
    user = User.query.first()
    db.session.delete(user)
    db.session.commit()

def query_tables():
    first_user = User.query.first()

    print("First user")
    for order in first_user.orders:
        print(f"Order ID: {order.id} Total: {order.total}")

    second_user = User.query.filter_by(id=2).first()# use the filter_by method to filter the query by a specific column value, this will return a query object that we can then call first on to get the first result that matches the filter criteria

    print("Second user")
    for order in second_user.orders:
        print(f"Order ID: {order.id} Total: {order.total}")    

def add_products_to_orders():
    first_product = Product(name="First")
    second_product = Product(name="Second")
    third_product  = Product(name="Third")

    db.session.add_all([first_product, second_product, third_product])

    first_order = Order.query.first()
    first_order.products.append(first_product) # use the append method to add a product to the products relationship of the order, this will automatically create a new entry in the order_product association table that links the order and product together
    first_order.products.append(second_product)

    db.session.commit()

def query_order_products():
    first_order = Order.query.filter_by(id=1).first()
    second_order = Order.query.filter_by(id=2).first()

    print("First order products")
    for product in first_order.products:
        print(f"Product name: {product.name}")

    print("Second order products")
    for product in second_order.products:
        print(f"Product name: {product.name}")

def get_all_users():
    users = User.query.all()

    for user in users:
        print(f"User name: {user.name}")

    user_count = User.query.count()

    print(f"User count: {user_count}")