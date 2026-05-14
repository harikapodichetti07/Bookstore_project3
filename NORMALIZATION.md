# Normalization Report

## Original Schema (Before 3NF)
Customers(customer_id, name, email, created_date)
Books(book_id, title, author, price, published_date, created_date)
Orders(order_id, customer_id, order_date, total_amount, created_date)
Order_Items(item_id, order_id, book_id, quantity, price, line_total, created_date)

---

## Original Functional Dependencies

**Customers:**
- customer_id → name, email, created_date

**Books:**
- book_id → title, author, price, published_date, created_date

**Orders:**
- order_id → customer_id, order_date, total_amount, created_date

**Order_Items:**
- item_id → order_id, book_id, quantity, price, created_date
- quantity, price → line_total (derived column)

---

## Anomaly Identification

### line_total in Order_Items
- **Update Anomaly:** If price is updated, line_total becomes stale
  unless manually recalculated.
- **Insertion Anomaly:** A wrong line_total can be inserted that does
  not match quantity * price.
- **Root Cause:** line_total is transitively dependent on quantity
  and price, not directly on item_id. This violates 3NF.

### total_amount in Orders
- **Update Anomaly:** Adding a new Order_Item does not automatically
  update total_amount in the Orders table.
- **Deletion Anomaly:** Deleting an Order_Item leaves total_amount
  incorrect unless manually fixed.
- **Root Cause:** total_amount is derived from SUM(Order_Items.price * quantity)
  and is transitively dependent on data in another table. This violates 3NF.

---

## Decomposition Steps

### Step 1 - Check 1NF
All tables have atomic columns and a primary key. Already in 1NF. ✅

### Step 2 - Check 2NF
All primary keys are single-column, so partial dependencies cannot exist.
Already in 2NF. ✅

### Step 3 - Check 3NF
Two violations found:

**Violation 1:** Order_Items.line_total
- Dependency: item_id → quantity → line_total (transitive)
- Fix: Remove line_total column. Calculate dynamically as quantity * price.

**Violation 2:** Orders.total_amount
- Dependency: order_id → Order_Items → total_amount (transitive)
- Fix: Remove total_amount column. Calculate dynamically using:
  SELECT SUM(quantity * price) FROM Order_Items WHERE order_id = ?

---

## Final Relational Schema (3NF)

Customers(customer_id PK, name, email, created_date)
Books(book_id PK, title, author, price, published_date, created_date)
Orders(order_id PK, customer_id FK→Customers, order_date, created_date)
Order_Items(item_id PK, order_id FK→Orders, book_id FK→Books,
            quantity, price, created_date)

No derived or transitively dependent columns remain.
All non-key attributes depend only on the primary key. 3NF achieved. ✅