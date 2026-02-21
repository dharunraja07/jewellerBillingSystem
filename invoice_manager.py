import sqlite3
from datetime import datetime

DB_NAME = "jewellery.db"


def connect_db():
    return sqlite3.connect(DB_NAME)


def create_invoice_table():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS invoices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            invoice_no TEXT,
            customer_name TEXT,
            mobile TEXT,
            subtotal REAL,
            cgst REAL,
            sgst REAL,
            grand_total REAL,
            date TEXT
        )
    """)

    conn.commit()
    conn.close()


def save_invoice(invoice_no, name, mobile, subtotal, cgst, sgst, grand_total):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO invoices (
            invoice_no, customer_name, mobile,
            subtotal, cgst, sgst, grand_total, date
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        invoice_no,
        name,
        mobile,
        subtotal,
        cgst,
        sgst,
        grand_total,
        datetime.now().strftime("%Y-%m-%d")
    ))

    conn.commit()
    conn.close()


def get_dashboard_data():
    conn = connect_db()
    cursor = conn.cursor()

    # Total Sales Today
    today = datetime.now().strftime("%Y-%m-%d")

    cursor.execute("SELECT SUM(grand_total) FROM invoices WHERE date=?", (today,))
    today_sales = cursor.fetchone()[0] or 0

    # Total Invoices Today
    cursor.execute("SELECT COUNT(*) FROM invoices WHERE date=?", (today,))
    today_invoices = cursor.fetchone()[0]

    # Total Customers
    cursor.execute("SELECT COUNT(*) FROM customers")
    total_customers = cursor.fetchone()[0]

    # Monthly Sales
    month = datetime.now().strftime("%Y-%m")
    cursor.execute("SELECT SUM(grand_total) FROM invoices WHERE date LIKE ?", (month + "%",))
    monthly_sales = cursor.fetchone()[0] or 0

    conn.close()

    return {
        "today_sales": today_sales,
        "today_invoices": today_invoices,
        "total_customers": total_customers,
        "monthly_sales": monthly_sales
    }
def get_invoices_by_mobile(mobile):
    conn = get_db_connection()
    invoices = conn.execute(
        "SELECT * FROM invoices WHERE mobile = ? ORDER BY id DESC",
        (mobile,)
    ).fetchall()
    conn.close()
    return invoices