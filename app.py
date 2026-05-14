from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Customer, Book, Order, OrderItem
from sqlalchemy import func
from datetime import date

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bookstore.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'bookstore-secret-key'
db.init_app(app)

def seed_data():
    """Auto-populate the database with sample data if it is empty."""

    if Customer.query.count() == 0:
        customers = [
            Customer(name='John Smith',    email='john@example.com',  created_date=date(2024,1,1)),
            Customer(name='Mary Johnson',  email='mary@example.com',  created_date=date(2023,1,5)),
            Customer(name='David Lee',     email='david@example.com', created_date=date(2023,1,10)),
            Customer(name='Sara Brown',    email='sara@example.com',  created_date=date(2024,2,1)),
            Customer(name='James Wilson',  email='james@example.com', created_date=date(2024,2,10)),
        ]
        db.session.add_all(customers)
        db.session.commit()

    if Book.query.count() == 0:
        books = [
            Book(book_id=101, title='Python Basics',    author='Milk Ross',     price=29.99, published_date=date(2023,1,1),  created_date=date(2024,1,1)),
            Book(book_id=102, title='SQL Guide',        author='Rachel Green',  price=39.99, published_date=date(2022,6,1),  created_date=date(2024,1,1)),
            Book(book_id=103, title='Data Science',     author='Ross Geller',   price=49.99, published_date=date(2021,9,1),  created_date=date(2024,1,1)),
            Book(book_id=104, title='AI Introduction',  author='Monica Bing',   price=59.99, published_date=date(2020,3,1),  created_date=date(2024,1,1)),
            Book(book_id=105, title='Machine Learning', author='Chandler Bing', price=69.99, published_date=date(2019,7,1),  created_date=date(2024,1,1)),
        ]
        db.session.add_all(books)
        db.session.commit()

    if Order.query.count() == 0:
        orders = [
            Order(order_id=201, customer_id=1, order_date=date(2024,3,1),  created_date=date(2024,3,1)),
            Order(order_id=202, customer_id=2, order_date=date(2024,3,2),  created_date=date(2024,3,2)),
            Order(order_id=203, customer_id=3, order_date=date(2024,3,3),  created_date=date(2024,3,3)),
            Order(order_id=204, customer_id=4, order_date=date(2023,3,4),  created_date=date(2024,3,4)),
            Order(order_id=205, customer_id=5, order_date=date(2024,3,5),  created_date=date(2024,3,5)),
        ]
        db.session.add_all(orders)
        db.session.commit()

    if OrderItem.query.count() == 0:
        items = [
            OrderItem(item_id=301, order_id=201, book_id=101, quantity=2, price=29.99, created_date=date(2024,3,1)),
            OrderItem(item_id=302, order_id=202, book_id=102, quantity=1, price=39.99, created_date=date(2024,3,2)),
            OrderItem(item_id=303, order_id=203, book_id=103, quantity=1, price=49.99, created_date=date(2024,3,3)),
            OrderItem(item_id=304, order_id=204, book_id=104, quantity=1, price=59.99, created_date=date(2024,3,4)),
            OrderItem(item_id=305, order_id=205, book_id=105, quantity=1, price=69.99, created_date=date(2024,3,5)),
        ]
        db.session.add_all(items)
        db.session.commit()

with app.app_context():
    db.create_all()
    seed_data()

# ─────────────────────────────────────────────
# DASHBOARD
# ─────────────────────────────────────────────
@app.route('/')
def dashboard():
    total_customers = db.session.query(func.count(Customer.customer_id)).scalar()
    total_books     = db.session.query(func.count(Book.book_id)).scalar()
    total_orders    = db.session.query(func.count(Order.order_id)).scalar()
    total_revenue   = db.session.query(
        func.sum(OrderItem.quantity * OrderItem.price)
    ).scalar() or 0
    avg_book_price  = db.session.query(func.avg(Book.price)).scalar() or 0

    top_customers = db.session.query(
        Customer.name,
        func.count(Order.order_id).label('order_count')
    ).join(Order, Customer.customer_id == Order.customer_id)\
     .group_by(Customer.customer_id)\
     .order_by(func.count(Order.order_id).desc())\
     .limit(3).all()

    return render_template('dashboard.html',
        total_customers=total_customers,
        total_books=total_books,
        total_orders=total_orders,
        total_revenue=round(float(total_revenue), 2),
        avg_book_price=round(float(avg_book_price), 2),
        top_customers=top_customers
    )

# ─────────────────────────────────────────────
# CUSTOMERS
# ─────────────────────────────────────────────
@app.route('/customers')
def customers():
    all_customers = Customer.query.all()
    return render_template('customers.html', customers=all_customers)

@app.route('/customers/add', methods=['POST'])
def add_customer():
    name  = request.form.get('name', '').strip()
    email = request.form.get('email', '').strip()
    if not name or not email:
        flash('Name and email are required.', 'danger')
        return redirect(url_for('customers'))
    if Customer.query.filter_by(email=email).first():
        flash('A customer with that email already exists.', 'danger')
        return redirect(url_for('customers'))
    new_customer = Customer(name=name, email=email, created_date=date.today())
    db.session.add(new_customer)
    db.session.commit()
    flash('Customer added successfully!', 'success')
    return redirect(url_for('customers'))

@app.route('/customers/edit/<int:id>', methods=['POST'])
def edit_customer(id):
    c     = Customer.query.get_or_404(id)
    name  = request.form.get('name', '').strip()
    email = request.form.get('email', '').strip()
    if not name or not email:
        flash('Name and email are required.', 'danger')
        return redirect(url_for('customers'))
    c.name  = name
    c.email = email
    db.session.commit()
    flash('Customer updated successfully!', 'success')
    return redirect(url_for('customers'))

@app.route('/customers/delete/<int:id>')
def delete_customer(id):
    c = Customer.query.get_or_404(id)
    db.session.delete(c)
    db.session.commit()
    flash('Customer deleted.', 'warning')
    return redirect(url_for('customers'))

# ─────────────────────────────────────────────
# BOOKS
# ─────────────────────────────────────────────
@app.route('/books')
def books():
    all_books = Book.query.all()
    return render_template('books.html', books=all_books)

@app.route('/books/add', methods=['POST'])
def add_book():
    title  = request.form.get('title', '').strip()
    author = request.form.get('author', '').strip()
    price  = request.form.get('price', '').strip()
    if not title or not author or not price:
        flash('All fields are required.', 'danger')
        return redirect(url_for('books'))
    try:
        price = float(price)
        if price < 0:
            raise ValueError
    except ValueError:
        flash('Price must be a valid non-negative number.', 'danger')
        return redirect(url_for('books'))
    new_book = Book(title=title, author=author, price=price,
                    created_date=date.today())
    db.session.add(new_book)
    db.session.commit()
    flash('Book added successfully!', 'success')
    return redirect(url_for('books'))

@app.route('/books/edit/<int:id>', methods=['POST'])
def edit_book(id):
    b      = Book.query.get_or_404(id)
    title  = request.form.get('title', '').strip()
    author = request.form.get('author', '').strip()
    price  = request.form.get('price', '').strip()
    if not title or not author or not price:
        flash('All fields are required.', 'danger')
        return redirect(url_for('books'))
    try:
        price = float(price)
        if price < 0:
            raise ValueError
    except ValueError:
        flash('Price must be a valid non-negative number.', 'danger')
        return redirect(url_for('books'))
    b.title  = title
    b.author = author
    b.price  = price
    db.session.commit()
    flash('Book updated successfully!', 'success')
    return redirect(url_for('books'))

@app.route('/books/delete/<int:id>')
def delete_book(id):
    b = Book.query.get_or_404(id)
    db.session.delete(b)
    db.session.commit()
    flash('Book deleted.', 'warning')
    return redirect(url_for('books'))

# ─────────────────────────────────────────────
# ORDERS (with Transaction Logic)
# ─────────────────────────────────────────────
@app.route('/orders')
def orders():
    all_orders    = Order.query.all()
    all_customers = Customer.query.all()
    all_books     = Book.query.all()
    return render_template('orders.html',
        orders=all_orders,
        customers=all_customers,
        books=all_books
    )

@app.route('/orders/add', methods=['POST'])
def add_order():
    """
    TRANSACTION LOGIC:
    Step 1 - Create the Order record
    Step 2 - Create the Order_Item record linked to that order
    Both steps are committed together. If either fails, both roll back.
    """
    customer_id = request.form.get('customer_id', '').strip()
    book_id     = request.form.get('book_id', '').strip()
    quantity    = request.form.get('quantity', '').strip()

    if not customer_id or not book_id or not quantity:
        flash('All fields are required.', 'danger')
        return redirect(url_for('orders'))
    try:
        quantity = int(quantity)
        if quantity <= 0:
            raise ValueError
    except ValueError:
        flash('Quantity must be a positive whole number.', 'danger')
        return redirect(url_for('orders'))

    try:
        book = Book.query.get_or_404(int(book_id))

        # STEP 1: Create the Order
        new_order = Order(
            customer_id=int(customer_id),
            order_date=date.today(),
            created_date=date.today()
        )
        db.session.add(new_order)
        db.session.flush()  # Get order_id before committing

        # STEP 2: Create the Order Item (only after order exists)
        new_item = OrderItem(
            order_id=new_order.order_id,
            book_id=book.book_id,
            quantity=quantity,
            price=book.price,
            created_date=date.today()
        )
        db.session.add(new_item)
        db.session.commit()  # Both committed together
        flash('Order placed successfully!', 'success')

    except Exception as e:
        db.session.rollback()
        flash(f'Transaction failed and was rolled back: {e}', 'danger')

    return redirect(url_for('orders'))

@app.route('/orders/delete/<int:id>')
def delete_order(id):
    o = Order.query.get_or_404(id)
    db.session.delete(o)
    db.session.commit()
    flash('Order deleted.', 'warning')
    return redirect(url_for('orders'))

if __name__ == '__main__':
    app.run(debug=True)
