# AI Assistance Log

## Entry 1

- **Tool:** Claude (Anthropic)
- **Prompt:** "Help me structure a Flask bookstore app with SQLAlchemy models
  for Customers, Books, Orders, and Order_Items"
- **AI Output:** Provided models.py with SQLAlchemy model classes and
  relationships between tables.
- **My Modifications:** Adjusted column names to match my existing database
  schema from Project 2. Added the line_total property as a computed
  value instead of a stored column to satisfy 3NF requirements.

## Entry 2

- **Tool:** Claude (Anthropic)
- **Prompt:** "Help me write Flask routes for CRUD operations with
  server-side validation"
- **AI Output:** Provided app.py with routes for add, edit, delete
  operations and flash messages for user feedback.
- **My Modifications:** Added specific validation rules for my schema
  (non-negative price check, duplicate email check). Adapted the
  transaction logic in add_order() to match my Order/OrderItem structure.

## Entry 3

- **Tool:** Claude (Anthropic)
- **Prompt:** "Help me write Bootstrap 5 HTML templates with modals
  for a bookstore CRUD app"
- **AI Output:** Provided base.html, dashboard.html, customers.html,
  books.html, and orders.html templates.
- **My Modifications:** Customized the dashboard cards to show the
  specific aggregate stats required by the project. Added the top
  customers table and adjusted all form fields to match my exact
  database column names.
