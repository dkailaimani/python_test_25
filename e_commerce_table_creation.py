//Tables created for MySQL database from Flask

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
