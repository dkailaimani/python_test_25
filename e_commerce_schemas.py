Schemas for tables to be created in MySQL database
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
