from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from cafe_backend import CafeBackend
import json

app = Flask(__name__)
app.secret_key = "cafe_secret"
cafe = CafeBackend()

@app.route('/')
def index():
    menu = cafe.get_menu()
    return render_template('index.html', menu=menu)

@app.route('/place_order', methods=['POST'])
def place_order():
    # Expecting simple form or JSON. 
    # For this professional implementation, we'll use a dynamic cart model in the UI.
    try:
        cart_data = request.form.get('cart')
        if not cart_data:
            return redirect(url_for('index'))
            
        cart = json.loads(cart_data)
        items = [(int(mid), int(qty)) for mid, qty in cart.items() if int(qty) > 0]
        
        if not items:
            flash("Empty cart!", "warning")
            return redirect(url_for('index'))
            
        order_id, total = cafe.create_order(items)
        flash(f"Order #{order_id} placed! Total: ${total:.2f}", "success")
        return redirect(url_for('orders'))
    except Exception as e:
        flash(f"Error: {str(e)}", "danger")
        return redirect(url_for('index'))

@app.route('/orders')
def orders():
    all_orders = cafe.get_orders()
    return render_template('orders.html', orders=all_orders)

@app.route('/order/<int:oid>')
def order_details(oid):
    details = cafe.get_order_details(oid)
    return jsonify(details)

@app.route('/menu_admin')
def menu_admin():
    menu = cafe.get_menu()
    return render_template('menu_admin.html', menu=menu)

@app.route('/add_item', methods=['POST'])
def add_item():
    name = request.form.get('name')
    price = float(request.form.get('price'))
    category = request.form.get('category')
    cafe.add_menu_item(name, price, category)
    flash("Item added!", "success")
    return redirect(url_for('menu_admin'))

if __name__ == '__main__':
    app.run(debug=True, port=5002)
