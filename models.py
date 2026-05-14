from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Customer(db.Model):
    __tablename__ = 'customers'
    customer_id  = db.Column(db.Integer, primary_key=True)
    name         = db.Column(db.String(100), nullable=False)
    email        = db.Column(db.String(100), nullable=False, unique=True)
    created_date = db.Column(db.Date)
    orders       = db.relationship('Order', backref='customer',
                                   cascade='all, delete-orphan')

class Book(db.Model):
    __tablename__ = 'books'
    book_id        = db.Column(db.Integer, primary_key=True)
    title          = db.Column(db.String(150), nullable=False)
    author         = db.Column(db.String(100), nullable=False)
    price          = db.Column(db.Numeric(8, 2), nullable=False)
    published_date = db.Column(db.Date)
    created_date   = db.Column(db.Date)

class Order(db.Model):
    __tablename__ = 'orders'
    order_id     = db.Column(db.Integer, primary_key=True)
    customer_id  = db.Column(db.Integer,
                             db.ForeignKey('customers.customer_id'),
                             nullable=False)
    order_date   = db.Column(db.Date)
    created_date = db.Column(db.Date)
    items        = db.relationship('OrderItem', backref='order',
                                   cascade='all, delete-orphan')

class OrderItem(db.Model):
    __tablename__ = 'order_items'
    item_id      = db.Column(db.Integer, primary_key=True)
    order_id     = db.Column(db.Integer,
                             db.ForeignKey('orders.order_id'),
                             nullable=False)
    book_id      = db.Column(db.Integer,
                             db.ForeignKey('books.book_id'),
                             nullable=False)
    quantity     = db.Column(db.Integer, nullable=False)
    price        = db.Column(db.Numeric(8, 2), nullable=False)
    created_date = db.Column(db.Date)
    book         = db.relationship('Book')

    @property
    def line_total(self):
        return float(self.quantity) * float(self.price)
