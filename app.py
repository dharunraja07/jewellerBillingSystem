import os
from flask import Flask, render_template, request, send_file, jsonify

from billing import calculate_item
from pdf_generator import generate_invoice

from customer_manager import (
    create_customer_table,
    add_customer,
    get_customer_by_mobile,
    search_customers
)

from invoice_manager import (
    create_invoice_table,
    save_invoice,
    get_dashboard_data
)

app = Flask(__name__)


# ==============================
# HOME
# ==============================
@app.route("/")
def home():
    return render_template("index.html")


# ==============================
# SEARCH CUSTOMER API
# ==============================
@app.route("/search_customer")
def search_customer():
    query = request.args.get("q", "")
    results = search_customers(query)
    return jsonify(results)


# ==============================
# AUTO-FILL CUSTOMER API
# ==============================
@app.route("/get_customer/<mobile>")
def get_customer(mobile):
    customer = get_customer_by_mobile(mobile)

    if customer:
        return jsonify(customer)

    return jsonify({"error": "Customer Not Found"})


# ==============================
# ADMIN DASHBOARD
# ==============================
@app.route("/admin")
def admin_dashboard():
    data = get_dashboard_data()
    return render_template("admin.html", data=data)


# ==============================
# GENERATE BILL
# ==============================
@app.route("/generate", methods=["POST"])
def generate():

    name = request.form.get("name")
    mobile = request.form.get("mobile")
    city = request.form.get("city")
    address = request.form.get("address")
    gold_rate = float(request.form.get("gold_rate", 0))

    # ✅ ALWAYS insert/update customer
    if mobile:
        add_customer(name, mobile, city, address)

    items = []
    subtotal = 0

    for i in range(1, 50):

        item_name = request.form.get(f"item_name_{i}")

        if item_name:

            weight = float(request.form.get(f"weight_{i}", 0))
            wastage = float(request.form.get(f"wastage_{i}", 0))
            making = float(request.form.get(f"making_{i}", 0))
            huid = request.form.get(f"huid_{i}", "")

            result = calculate_item(weight, gold_rate, wastage, making)

            items.append({
                "name": item_name,
                "huid": huid,
                "weight": weight,
                "wastage": wastage,
                "gold_rate": gold_rate,
                "making": making,
                "total": result["total"]
            })

            subtotal += result["total"]

    # GST 3%
    cgst = subtotal * 0.015
    sgst = subtotal * 0.015
    grand_total = subtotal + cgst + sgst

    # Invoice Counter
    invoice_file = "invoice_counter.txt"

    if not os.path.exists(invoice_file):
        with open(invoice_file, "w") as f:
            f.write("1")

    with open(invoice_file, "r") as f:
        number = int(f.read().strip())

    invoice_no = str(number).zfill(4)

    with open(invoice_file, "w") as f:
        f.write(str(number + 1))

    # Generate PDF
    pdf_file = generate_invoice(
        name,
        invoice_no,
        items,
        subtotal,
        cgst,
        sgst,
        grand_total
    )

    # Save Invoice
    save_invoice(
        invoice_no,
        name,
        mobile,
        subtotal,
        cgst,
        sgst,
        grand_total
    )

    return send_file(pdf_file, as_attachment=True)


# ==============================
# START APPLICATION
# ==============================
if __name__ == "__main__":
    create_customer_table()
    create_invoice_table()
    app.run(debug=True)