import copy
from functools import wraps
import threading
from typing import Any, Dict, List, Optional
from flask import Blueprint, Flask, jsonify, render_template, send_from_directory, request
from const.config import ITEMS, ORDERS
from waitress import serve
from const.config import *
import flask_cors
from utils.order_calculator import get_bulk_order_quote

API_KEY = "qqww22ttzxqwr6778"  # Change this to your desired key
ALLOWED_KEYS = {API_KEY}

def is_valid_api_key(key: str | None) -> bool:
    if not key:
        return False
    return key in ALLOWED_KEYS

def require_api_key(view_func):
    @wraps(view_func)
    def wrapped(*args, **kwargs):
        key = request.headers.get("X-API-KEY")
        if not is_valid_api_key(key):
            app.logger.debug("API key invalid or missing: %s", key)
            return jsonify({"error": "Invalid or missing API key"}), 401
        return view_func(*args, **kwargs)
    return wrapped


_CURRENT_ORDERS: Dict[str, List[Dict[str, Any]]] = {}
_CURRENT_ORDERS_LOCK = threading.Lock()

def set_current_orders(orders_map: Dict[str, List[Dict[str, Any]]]) -> None:
    global _CURRENT_ORDERS
    with _CURRENT_ORDERS_LOCK:
        _CURRENT_ORDERS = copy.deepcopy(orders_map)

def get_current_orders() -> Dict[str, List[Dict[str, Any]]]:
    with _CURRENT_ORDERS_LOCK:
        return copy.deepcopy(_CURRENT_ORDERS)

def get_orders_for_user(email: str) -> List[Dict[str, Any]]:
    with _CURRENT_ORDERS_LOCK:
        return copy.deepcopy(_CURRENT_ORDERS.get(email, []))

def set_orders_for_user(email: str, orders: List[Dict[str, Any]]) -> None:
    with _CURRENT_ORDERS_LOCK:
        _CURRENT_ORDERS[email] = copy.deepcopy(orders)

def add_order_for_user(email: str, order: Dict[str, Any]) -> None:
    with _CURRENT_ORDERS_LOCK:
        _CURRENT_ORDERS.setdefault(email, []).append(copy.deepcopy(order))

def find_order_for_user(email: str, order_id: str) -> Optional[Dict[str, Any]]:
    with _CURRENT_ORDERS_LOCK:
        orders = _CURRENT_ORDERS.get(email, [])
        for o in orders:
            if o.get("id") == order_id:
                return copy.deepcopy(o)
    return None

def update_order_for_user(email: str, order_id: str, updates: Dict[str, Any]) -> bool:
    with _CURRENT_ORDERS_LOCK:
        orders = _CURRENT_ORDERS.get(email)
        if not orders:
            return False
        for i, o in enumerate(orders):
            if o.get("id") == order_id:
                updated = dict(o)  # shallow copy of order dict
                updated.update(updates)
                orders[i] = copy.deepcopy(updated)
                return True
    return False

def remove_order_for_user(email: str, order_id: str) -> bool:
    with _CURRENT_ORDERS_LOCK:
        orders = _CURRENT_ORDERS.get(email)
        if not orders:
            return False
        for i, o in enumerate(orders):
            if o.get("id") == order_id:
                del orders[i]
                # cleanup empty list
                if not orders:
                    _CURRENT_ORDERS.pop(email, None)
                return True
    return False

def recalc_order_total(order: Dict[str, Any]) -> float:
    items = order.get("items", [])
    total = 0.0
    for it in items:
        price = float(it.get("price", 0) or 0)
        qty = int(it.get("quantity", 0) or 0)
        subtotal = round(price * qty, 2)
        it["subtotal"] = subtotal
        total += subtotal
    return round(total, 2)


def clear_orders_for_user(email: str) -> None:
    with _CURRENT_ORDERS_LOCK:
        _CURRENT_ORDERS.pop(email, None)

def clear_all_orders() -> None:
    with _CURRENT_ORDERS_LOCK:
        _CURRENT_ORDERS.clear()


_CURRENT_USER = None
_CURRENT_USER_LOCK = threading.Lock()
def set_current_user(user_obj):
    with _CURRENT_USER_LOCK:
        global _CURRENT_USER
        _CURRENT_USER = user_obj

def get_current_user():
    with _CURRENT_USER_LOCK:
        if _CURRENT_USER: return _CURRENT_USER
        else: return {
            "email": 'anto.sf3688@gmail.com',
            "password": 'password',
        }

def clear_current_user():
    with _CURRENT_USER_LOCK:
        global _CURRENT_USER
        _CURRENT_USER = None

app = Flask(__name__, static_folder='build', template_folder='build')
flask_cors.CORS(app)

# Initialize orders from config
for order_entry in ORDERS:
    for email, orders in order_entry.items():
        set_orders_for_user(email, orders)

api = Blueprint("api", __name__, url_prefix="/api")
order = Blueprint("order", __name__, url_prefix="/order")

# List all items
@api.route('/items', methods=['GET'])
@require_api_key
def get_items():
    return jsonify(ITEMS)

@app.route('/static/images/<path:filename>')
def serve_product_image(filename):
    try:
        return send_from_directory('images', filename)
    except Exception:
        # Return a default image or 404
        return send_from_directory('images', 'default-product.png')

@app.route('/logout', methods=['POST'])
@require_api_key
def logout():

    user = get_current_user()
    if user:
        clear_current_user()
        return jsonify({"status": "ok"}), 200
    return jsonify({"error": "No user logged in"}), 401

from flask import request, jsonify
from datetime import datetime

@app.route('/login_user', methods=['POST'])
@require_api_key
def login():
    try:
        data = request.get_json(silent=True) or {}
        email = data.get('email', '').strip()
        password = data.get('password', '')

        if not email or not password:
            return jsonify({'error': 'Email / Password is missing.'}), 400
        
        if '@' not in email or '.' not in email.split('@')[-1]:
            return jsonify({'error': 'Invalid email format.'}), 400
        
        user_obj = {
            "email": email,
            "password": password,
        }
        set_current_user(user_obj)

        print(f"User logged in: {email}")
        return jsonify({"status": "ok", "user": {"email": email}}), 200

    except Exception as e:
        print(f"Login error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

# Get item by id
@api.route('/items/<string:item_id>', methods=['GET'])
@require_api_key
def get_item(item_id):
    for item in ITEMS:
        if item['id'] == item_id:
            return jsonify(item)
    return jsonify({'error': 'Item not found'}), 404

# List orders for current user
@api.route('/orders', methods=['GET'])
@require_api_key
def get_orders():

    user = get_current_user()
    if not user:
        return jsonify({'error': 'No user logged in'}), 401

    orders = get_orders_for_user(user['email'])
    return jsonify(orders), 200


# Search items by name or category
@api.route('/items/search')
@require_api_key
def search_items():
    q = request.args.get('q', '').lower()
    if not q:
        return jsonify({'error': 'Missing search query'}), 400
    results = [item for item in ITEMS if q in item['name'].lower() or q in item['category'].lower()]
    return jsonify(results)

# Gets Order Status using Order ID
@order.route('/status', methods=['GET'])
@require_api_key
def get_order_status():

    try:
        order_id = request.args.get('order_id')
        if not order_id:
            return jsonify({'error': 'Missing order_id parameter'}), 400

        user = get_current_user()
        if not user:
            return jsonify({'error': 'No user logged in'}), 401

        order = find_order_for_user(user['email'], order_id)
        if not order:
            return jsonify({'error': 'Order not found'}), 404

        return jsonify({"status": order['status']}), 200
    except Exception as e:
        print(f"Error fetching order status: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@order.route('/calculate-bulk', methods=['POST'])
@require_api_key
def calculate_bulk_order():
    """
    Calculate bulk order prices with applicable discounts

    Expected request body:
    {
        "items": [
            {"name": "Premium Arabica Coffee Beans", "quantity": 10},
            {"name": "Gourmet Coffee Cookies", "quantity": 5}
        ]
    }
    """
    try:
        data = request.get_json(silent=True)
        if not data or 'items' not in data:
            return jsonify({'error': 'Missing items list in request'}), 400

        items = data['items']
        if not isinstance(items, list):
            return jsonify({'error': 'Items must be a list'}), 400

        processed_items: List[Dict] = []
        for idx, item in enumerate(items):
            if not isinstance(item, dict):
                return jsonify({'error': f'Item at index {idx} must be an object'}), 400

            name = item.get('name')
            raw_qty = item.get('quantity')

            if not isinstance(name, str) or not name.strip():
                return jsonify({'error': f'Invalid or missing name for item at index {idx}'}), 400

            # Coerce quantity to number (accept string numbers like "200")
            try:
                # allow integers and floats; treat float quantities as numeric then cast to int
                if raw_qty is not None:
                    qty_num = float(raw_qty)
                    if qty_num <= 0:
                        return jsonify({'error': f'Quantity must be a positive number for item "{name}"'}), 400

                    # Convert to int if desired (rounding down); adjust if you prefer rounding
                    quantity = int(qty_num)

                    processed_items.append({
                        'name': name.strip(),
                        'quantity': quantity
                    })

                else:
                    return jsonify({'error': f'Invalid quantity for item "{name}"'}), 400
            except (TypeError, ValueError):
                return jsonify({'error': f'Invalid quantity for item "{name}"'}), 400

        # Ensure we processed at least one item
        if not processed_items:
            return jsonify({'error': 'No valid items provided'}), 400

        # Calculate the quote using the processed_items list after processing all items
        quote = get_bulk_order_quote(processed_items)
        return jsonify(quote), 200

    except Exception as e:
        # Prefer structured logging in real apps
        print(f"Error calculating bulk order: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@order.route('/update-shipping', methods=['POST'])
@require_api_key
def update_shipping_address():
    """
    Update shipping address for an order
    
    Expected request body:
    {
        "shipping_address": "New shipping address",
        "order_id": "ORD20001"
    }
    """
    try:
        user = get_current_user()
        if not user:
            return jsonify({"error": "No user logged in"}), 401

        data = request.get_json()
        if not data or 'shipping_address' not in data:
            return jsonify({"error": "Missing shipping_address in request"}), 400

        new_address = data['shipping_address'].strip()
        if not new_address:
            return jsonify({"error": "Shipping address cannot be empty"}), 400
        order_id = data.get('order_id', '').strip()
        if not order_id:
            return jsonify({"error": "Missing order_id in request"}), 400
        # Find the order
        order = find_order_for_user(user["email"], order_id)
        if not order:
            return jsonify({"error": "Order not found"}), 404

        # Update only the shipping address
        success = update_order_for_user(user["email"], order_id, {
            "shipping_address": new_address
        })

        if not success:
            return jsonify({"error": "Failed to update shipping address"}), 500

        # Get updated order
        return jsonify({
            "message": "Shipping address updated successfully",
            "order_id": order_id,
            "new_shipping_address": new_address
        }), 200

    except Exception as e:
        print(f"Error updating shipping address: {e}")
        return jsonify({"error": "Internal server error"}), 500

@order.route('put_order/<string:order_id>', methods=['PUT'])
@require_api_key
def put_order(order_id: str):

    user = get_current_user()
    if not user:
        return jsonify({"error": "No user logged in"}), 401

    payload = request.get_json(silent=True)
    if not payload or not isinstance(payload, dict):
        return jsonify({"error": "JSON object required"}), 400

    # Validate required keys minimally for a full-order replace
    if "items" not in payload or not isinstance(payload["items"], list):
        return jsonify({"error": "items (list) required for full replace"}), 400

    existing = find_order_for_user(user["email"], order_id)
    if not existing:
        return jsonify({"error": "Order not found"}), 404

    # Build new order object preserving id and user-scoped fields as needed
    new_order = dict(payload)
    new_order["id"] = order_id
    if "order_total" not in new_order:
        new_order["order_total"] = recalc_order_total(new_order)
    else:
        # normalize subtotal values if provided
        recalc_order_total(new_order)

    success = update_order_for_user(user["email"], order_id, new_order)
    if not success:
        return jsonify({"error": "Failed to replace order"}), 500

    updated = find_order_for_user(user["email"], order_id)
    return jsonify(updated), 200

@api.route('/key')
def kb():
    return API_KEY

api.register_blueprint(order)

app.register_blueprint(api)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_frontend(path):
    try:
        if path:
            return send_from_directory('build', path)
    except Exception:
        pass
    return render_template('index.html')

if __name__ == '__main__':
    print("Server started")
    serve(app, host='0.0.0.0', port=8080)