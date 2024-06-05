
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import Schema, fields, ValidationError
from urllib.parse import quote_plus

app = Flask(__name__)
pw = 'XyZ$9#1@7QwEeTy'
updated_pw = quote_plus(pw)
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://root:{updated_pw}@localhost/e_commerce_db'

db = SQLAlchemy(app)
ma = Marshmallow(app)

class AuthorSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    birth_year = fields.Int(required=True)
    nationality = fields.Str(required=True)

class BookSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    genre = fields.Str(required=True)
    price = fields.Float(required=True)
    publication_date = fields.Date(required=True)
    author_id = fields.Int(required=True)

class CustomerSchema(ma.Schema):
    name = fields.String(required=True)
    email = fields.String(required=True)
    phone = fields.String(required=True)

    class Meta:
        fields = ("name", "email", "phone")

class CustomerAccountSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    username = fields.String(required=True)
    password = fields.String(required=True)
    customer_id = fields.Int(required=True)

class Order(ma.Schema):
    id = fields.Int(dump_only=True)
    date = fields.Date(required=True)
    customer_id = fields.Int(required=True)

class Product(ma.Schema):
    id = fields.Int(dump_only=True)
    username = fields.String(required=True)
    price = fields.Float(required=True)

author_schema = AuthorSchema()
authors_schema = AuthorSchema(many=True)

book_schema = BookSchema()
books_schema = BookSchema(many=True)

customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)

customer_account_schema = CustomerAccountSchema()
customer_accounts_schema = CustomerAccountSchema(many=True)

order_schema = Order()
orders_schema = Order(many=True)

product_schema = Product()
products_schema = Product(many=True)

class Customer(db.Model):
    __tablename__ = 'Customers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(320))
    phone = db.Column(db.String(15))
    orders = db.relationship('Order', backref='customer', lazy=True) 

class Book(db.Model):
    __tablename__ = 'Books'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('Authors.id'), nullable=False)
    genre = db.Column(db.String(255), nullable=False)
    publication_date = db.Column(db.Date, nullable=False)
    price = db.Column(db.Float, nullable=False)

class Author(db.Model):
    __tablename__ = 'Authors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    birth_year = db.Column(db.Integer, nullable=False)
    nationality = db.Column(db.String(255), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('Books.id'), nullable=False)

class Order(db.Model):
    __tablename__ = 'Orders'
    id = db.Column(db.Integer, primary_key=True) # Set primary_key to True
    date = db.Column(db.Date, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('Customers.id'), nullable=False)

# One-to-One
class CustomerAccount(db.Model):
    __tablename__ = 'Customer_Accounts'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('Customers.id'), nullable=False)
    customer = db.relationship('Customer', backref='customer_account', uselist=False)

# Initialize Many-to-Many association table
order_product = db.Table('Order_Product', 
        db.Column('order_id', db.Integer, db.ForeignKey('Orders.id'), primary_key=True),
        db.Column('product_id', db.Integer, db.ForeignKey('Products.id'), primary_key=True)
)   

class Product(db.Model):
    __tablename__ = 'Products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    orders = db.relationship('Order', secondary=order_product, backref=db.backref('products'))

@app.route('/customers', methods=['GET'])
def get_customers():
    customers = Customer.query.all()
    return customers_schema.jsonify(customers)

@app.route('/customers', methods=['POST'])
def add_customer():
    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400 
    
    new_customer = Customer(name=customer_data['name'], email=customer_data['email'], phone=customer_data['phone'])
    db.session.add(new_customer)
    db.session.commit()
    return jsonify({"message": "New Customer added successfully"}), 201

@app.route('/customers/<int:id>', methods=['PUT'])
def update_customer(id):
    customer = Customer.query.get_or_404(id)
    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    customer.name = customer_data['name']
    customer.email = customer_data['email']
    customer.phone = customer_data['phone']
    db.session.commit()
    return jsonify({"message": "Customer details updated successfully"}), 200

@app.route('/customers/<int:id>', methods=['DELETE'])
def delete_customer(id):
    customer = Customer.query.get_or_404(id)
    db.session.delete(customer)
    db.session.commit()
    return jsonify({"message": "Customer removed successfully"}), 200

@app.route('/customer_accounts', methods=['GET'])
def get_customer_accounts():
    customer_accounts = CustomerAccount.query.all()
    return customer_accounts_schema.jsonify(customer_accounts)

@app.route('/customer_accounts', methods=['POST'])
def add_customer_accounts():
    try:
        customer_account_data = customer_account_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400 
    
    new_customer_account = CustomerAccount(username=customer_account_data['username'], 
                                           password=customer_account_data['password'],
                                           customer_id=customer_account_data['customer_id'])
    db
@app.route('/customer_accounts/<int:id>', methods=['PUT'])
def update_customer_account(id):
    customer_account = CustomerAccount.query.get_or_404(id)
    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    customer_account.name = customer_data['username']
    customer_account.email = customer_data['password']
    customer_account.phone = customer_data['customer_id']
    db.session.commit()
    return jsonify({"message": "Customer Account details updated successfully"}), 200

@app.route('/customer_account/<int:id>', methods=['DELETE'])
def delete_customer(id):
    customer_account = CustomerAccount.query.get_or_404(id)
    db.session.delete(customer_account)
    db.session.commit()
    return jsonify({"message": "Customer Account removed successfully"}), 200

@app.route('/orders', methods=['GET'])
def get_orders():
    orders = Order.query.all()
    return jsonify(orders_schema.dump(orders))

@app.route('/orders', methods=['POST'])
def create_order():
    try:
        order_data = request.json
        new_order = Order(date=order_data['date'], customer_id=order_data['customer_id'])
        db.session.add(new_order)
        db.session.commit()
        return jsonify({"message": "New order created successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route('/orders/<int:id>', methods=['PUT'])
def update_order(id):
    order = Order.query.get_or_404(id)
    try:
        order_data = request.json
        order.date = order_data['date']
        order.customer_id = order_data['customer_id']
        db.session.commit()
        return jsonify({"message": "Order details updated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route('/orders/<int:id>', methods=['DELETE'])
def delete_order(id):
    order = Order.query.get_or_404(id)
    try:
        db.session.delete(order)
        db.session.commit()
        return jsonify({"message": "Order removed successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify(products_schema.dump(products))

@app.route('/products', methods=['POST'])
def create_product():
    try:
        product_data = request.json
        new_product = Product(name=product_data['name'], price=product_data['price'])
        db.session.add(new_product)
        db.session.commit()
        return jsonify({"message": "New product created successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route('/products/<int:id>', methods=['PUT'])
def update_product(id):
    product = Product.query.get_or_404(id)
    try:
        product_data = request.json
        product.name = product_data['name']
        product.price = product_data['price']
        db.session.commit()
        return jsonify({"message": "Product details updated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get_or_404(id)
    try:
        db.session.delete(product)
        db.session.commit()
        return jsonify({"message": "Product removed successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
