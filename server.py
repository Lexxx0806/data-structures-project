from flask import Flask, jsonify, request
from flask_cors import CORS
import random
import re
from helpers import Point, Rectangle
from quadtree import Quadtree

# 1. Data Loading
try:
    from listings_data import LISTING_TEMPLATES
except ImportError:
    print("⚠️ Error: listings_data.py not found.")
    LISTING_TEMPLATES = []

app = Flask(__name__)
CORS(app)

STREETS = ["Main St", "Broadway", "Park Ave", "Oak Ln", "Pine St", "Maple Dr", "Cedar Rd", "Sunset Blvd", "River Rd"]

def clean_price(price_str):
    """Robust price cleaner: removes symbols and ensures integer output"""
    if price_str is None: return 0
    if isinstance(price_str, int): return price_str
    cleaned = re.sub(r'[^\d]', '', str(price_str))
    return int(cleaned) if cleaned else 0

# 2. Quadtree Initialization
boundary = Rectangle(400, 300, 400, 300)
qt = Quadtree(boundary, 4) 

print(f"🌳 Generating listings from {len(LISTING_TEMPLATES)} templates...")

# 3. Populate the Tree
for i in range(200):
    x, y = random.randint(0, 800), random.randint(0, 600)
    
    if LISTING_TEMPLATES:
        tmpl = random.choice(LISTING_TEMPLATES)
        # Fix Price
        price_int = clean_price(tmpl.get("price", 0))
        title = tmpl.get("title", "Modern Apartment")
        
        # FIXED PHOTO LOGIC: Use a real fallback image if keys are missing
        # Some templates might use 'image' or 'img', we check both.
        main_photo = tmpl.get("img") or tmpl.get("image") or "https://images.unsplash.com/photo-1484154218962-a197022b5858?w=800"
        extra_photos = tmpl.get("images", [])
        
        # Ensure we always have a list of strings
        all_photos = [main_photo] + extra_photos
    else:
        price_int = 1000
        title = "Standard Apartment"
        all_photos = ["https://images.unsplash.com/photo-1484154218962-a197022b5858?w=800"]

    data = { 
        "id": i, 
        "title": title, 
        "type": "Apartment", 
        "price": price_int, 
        "address": f"{random.randint(10,999)} {random.choice(STREETS)}", 
        "photos": all_photos 
    }
    
    qt.insert(Point(x, y, data))

print(f"✅ Quadtree built with {len(qt)} nodes!")

# --- API ENDPOINTS (No changes needed here) ---
@app.route('/search', methods=['POST'])
def search():
    try:
        req_data = request.get_json(force=True, silent=True)
        if not req_data: return jsonify([])
        x = float(req_data.get('x', 0))
        y = float(req_data.get('y', 0))
        w = float(req_data.get('w', req_data.get('width', 0)))
        h = float(req_data.get('h', req_data.get('height', 0)))
        if w <= 0 or h <= 0: return jsonify([])
        found = []
        search_range = Rectangle(x + w/2, y + h/2, w/2, h/2)
        qt.query(search_range, found)
        return jsonify([{"x": p.x, "y": p.y, **p.data} for p in found])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/grid', methods=['GET'])
def get_grid():
    boxes = []
    def traverse(node):
        boxes.append({"x": node.boundary.x - node.boundary.w, "y": node.boundary.y - node.boundary.h, "w": node.boundary.w * 2, "h": node.boundary.h * 2})
        if node.divided:
            traverse(node.ne); traverse(node.nw); traverse(node.se); traverse(node.sw)
    traverse(qt)
    return jsonify(boxes)

if __name__ == '__main__': 
    app.run(debug=True, port=5000)
