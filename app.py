# app.py
# Very basic restaurant menu web app (Flask, single file)
# Run:  pip install flask
# Start: python app.py  -> open http://127.0.0.1:5000

from flask import Flask, request, render_template_string

app = Flask(__name__)

MENU = {
    "Starters": [
        {"id": "samosa", "name": "Veg Samosa (2 pcs)", "price": 40.0, "veg": True},
        {"id": "tikka", "name": "Chicken Tikka", "price": 180.0, "veg": False},
    ],
    "Mains": [
        {"id": "paneer", "name": "Paneer Butter Masala", "price": 240.0, "veg": True},
        {"id": "chkcurry", "name": "Chicken Curry", "price": 260.0, "veg": False},
    ],
    "Breads": [
        {"id": "naan", "name": "Butter Naan", "price": 35.0, "veg": True},
        {"id": "roti", "name": "Tandoori Roti", "price": 20.0, "veg": True},
    ],
    "Desserts": [
        {"id": "jamun", "name": "Gulab Jamun (2 pcs)", "price": 60.0, "veg": True},
    ],
    "Beverages": [
        {"id": "chaas", "name": "Masala Chaas", "price": 35.0, "veg": True},
        {"id": "cola", "name": "Cola", "price": 40.0, "veg": True},
    ],
}

# Flat lookup by id for quick access
ITEM_LOOKUP = {item["id"]: item for cat in MENU.values() for item in cat}

INDEX_TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Spice & Byte — Menu</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>
    body{font-family:system-ui,-apple-system,Segoe UI,Roboto,Arial,sans-serif; margin:2rem; background:#fafafa; color:#222}
    h1{margin-top:0}
    .menu{display:grid; gap:1.25rem}
    .card{background:#fff; border:1px solid #eee; border-radius:14px; padding:1rem; box-shadow:0 1px 2px rgba(0,0,0,0.04)}
    .cat{font-weight:700; margin-bottom:.5rem}
    .row{display:grid; grid-template-columns: 1fr auto auto; gap:.75rem; align-items:center; padding:.4rem 0; border-bottom:1px dashed #eee}
    .row:last-child{border-bottom:none}
    .pill{font-size:.8rem; padding:.15rem .5rem; border-radius:999px; border:1px solid #ddd; color:#444}
    .qty{width:70px}
    .price{min-width:90px; text-align:right}
    .legend{margin:.5rem 0 1rem 0; color:#666; font-size:.9rem}
    .submitbar{position:sticky; bottom:0; background:#fff; padding:1rem; border-top:1px solid #eee; margin-top:1rem}
    button{padding:.7rem 1rem; border:0; border-radius:10px; font-weight:600; cursor:pointer; background:#111; color:#fff}
    button:hover{opacity:.9}
  </style>
</head>
<body>
  <h1>Spice & Byte — Restaurant Menu</h1>
  <p class="legend">Select quantities and click <b>Review Order</b>. <span class="pill">🟢 veg</span> <span class="pill">🔴 non-veg</span></p>

  <form method="post" action="/order">
    <div class="menu">
      {% for category, items in menu.items() %}
        <div class="card">
          <div class="cat">{{ category }}</div>
          {% for item in items %}
            <div class="row">
              <div>
                {{ "🟢" if item.veg else "🔴" }} {{ item.name }}
              </div>
              <div class="price">₹ {{ '%.2f' % item.price }}</div>
              <div><input class="qty" type="number" min="0" max="20" value="0" name="qty_{{ item.id }}"></div>
            </div>
          {% endfor %}
        </div>
      {% endfor %}
    </div>

    <div class="submitbar">
      <button type="submit">Review Order</button>
    </div>
  </form>
</body>
</html>
"""

ORDER_TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Your Order — Spice & Byte</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>
    body{font-family:system-ui,-apple-system,Segoe UI,Roboto,Arial,sans-serif; margin:2rem; background:#fafafa; color:#222}
    h1{margin-top:0}
    table{width:100%; border-collapse:collapse; background:#fff; border:1px solid #eee; border-radius:14px; overflow:hidden}
    th,td{padding:.75rem 1rem; border-bottom:1px solid #eee; text-align:left}
    th:last-child, td:last-child{text-align:right}
    tfoot td{font-weight:700}
    .actions{margin-top:1rem}
    a,button{display:inline-block; margin-right:.5rem; padding:.6rem .9rem; border-radius:10px; text-decoration:none; font-weight:600}
    .back{background:#f1f1f1; color:#222}
    .confirm{background:#111; color:#fff; border:0}
    .empty{padding:1rem; background:#fff; border:1px solid #eee; border-radius:14px}
  </style>
</head>
<body>
  <h1>Your Order</h1>

  {% if items %}
    <table>
      <thead>
        <tr><th>Item</th><th>Qty</th><th>Price</th><th>Subtotal</th></tr>
      </thead>
      <tbody>
        {% for it in items %}
          <tr>
            <td>{{ it.name }}</td>
            <td>{{ it.qty }}</td>
            <td>₹ {{ '%.2f' % it.price }}</td>
            <td>₹ {{ '%.2f' % it.subtotal }}</td>
          </tr>
        {% endfor %}
      </tbody>
      <tfoot>
        <tr><td colspan="3">Total</td><td>₹ {{ '%.2f' % total }}</td></tr>
      </tfoot>
    </table>
    <div class="actions">
      <a class="back" href="/">⬅ Back to Menu</a>
      <button class="confirm" onclick="alert('This is a demo. No actual order is placed.')">Confirm Order</button>
    </div>
  {% else %}
    <div class="empty">
      You didn’t pick anything. <a class="back" href="/">Go back to the menu</a>.
    </div>
  {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET"])
def index():
    return render_template_string(INDEX_TEMPLATE, menu=MENU)

@app.route("/order", methods=["POST"])
def order():
    picked = []
    for key, value in request.form.items():
        if not key.startswith("qty_"):
            continue
        try:
            qty = int(value)
        except ValueError:
            qty = 0
        if qty <= 0:
            continue

        item_id = key.replace("qty_", "", 1)
        item = ITEM_LOOKUP.get(item_id)
        if not item:
            continue

        subtotal = qty * float(item["price"])
        picked.append({
            "id": item_id,
            "name": item["name"],
            "price": float(item["price"]),
            "qty": qty,
            "subtotal": subtotal
        })

    total = sum(i["subtotal"] for i in picked)
    return render_template_string(ORDER_TEMPLATE, items=picked, total=total)

if __name__ == "__main__":
    app.run(debug=True)
