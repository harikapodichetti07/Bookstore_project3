# Bookstore App

A full-stack bookstore management application built with Flask and SQLite.

## Project Description
This app allows users to manage customers, books, and orders for a bookstore.
It was built as part of CS665 Project 3 and demonstrates full CRUD operations,
transaction logic, data validation, and a summary dashboard.

## Tech Stack
- Python 3
- Flask
- SQLAlchemy
- SQLite
- HTML5, CSS3, Bootstrap 5
- Jinja2 Templates

## Installation Instructions

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd bookstore-project
```

### 2. Create Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

## Database Setup
The database is created automatically when you run the app.
SQLAlchemy will create all tables from the models defined in models.py.

To use the provided SQL schema manually:
```bash
sqlite3 bookstore.db < schema.sql
```

## Usage

### Run the App
```bash
python app.py
```

Open your browser and go to: **http://127.0.0.1:5000**

## Features
- Dashboard with COUNT, SUM, AVG aggregates
- Full CRUD for Customers, Books, and Orders
- Transaction logic: Order and Order_Item created atomically
- Server-side validation (no empty fields, no negative prices)
- One-to-Many relationship: Customer → Orders → Order_Items
