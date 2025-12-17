# server.py
from flask import Flask, jsonify, request
from flask_cors import CORS
import random
import re
from helpers import Point, Rectangle
from quadtree import Quadtree

# Import your data file
try:
    from listings_data import LISTING_TEMPLATES
except ImportError:
    print("⚠️ Error: listings_data.py not found. Please create it.")
    LISTING_TEMPLATES = []

app = Flask(__name__)
CORS(app)

STREETS = ["Main St", "Broadway", "Park Ave", "Oak Ln", "Pine St", "Maple Dr", "Cedar Rd", "Sunset Blvd", "River Rd"]

# Initialize Quadtree
# Canvas is 800x600. Center is (400, 300). Half-width/height is 400/300.
boundary = Rectangle(400, 300, 400, 300)
qt = Quadtree(boundary, 1)

def clean_price(price_str):
    """Helper to turn '$4,585' into integer 4585"""
    return int(re.sub(r'[^\d]', '', str(price_str)))

print(f"🌳 Generating listings from {len(LISTING_TEMPLATES)} templates...")

# Populate the tree
for i in range(200):
    x, y = random.randint(0, 800), random.randint(0, 600)
    
    if LISTING_TEMPLATES:
        tmpl = random.choice(LISTING_TEMPLATES)
        price_int = clean_price(tmpl["price"])
        photo_url = tmpl["img"]
        title = tmpl["title"]
    else:
        # Fallback if file is empty
        price_int = 1000
        photo_url = "https://placehold.co/600"
        title = "Generic Apartment"

    data = { 
        "id": i, 
        "title": title, 
        "type": "Apartment", 
        "price": price_int, 
        "address": f"{random.randint(10,999)} {random.choice(STREETS)}", 
        # Frontend expects a list of photos
        "photos": [photo_url, "https://placehold.co/600"] 
    }
    
    qt.insert(Point(x, y, data))

print(f"✅ Quadtree built with {len(qt)} nodes!")

@app.route('/')
def home(): 
    return "Server is running! Use /search endpoint."

@app.route('/search', methods=['POST'])
def search():
    try:
        data = request.get_json(force=True, silent=True)
        if not data:
            return jsonify({"error": "No data"}), 400
        
        # Safe extraction
        raw_x = data.get('x')
        raw_y = data.get('y')
        raw_w = data.get('w', data.get('width'))
        raw_h = data.get('h', data.get('height'))

        if any(v is None for v in [raw_x, raw_y, raw_w, raw_h]):
            return jsonify({"error": "Missing parameters"}), 400

        x, y, w, h = float(raw_x), float(raw_y), float(raw_w), float(raw_h)

        # Query Quadtree
        found = []
        
        # Conversion: Frontend sends Top-Left (x,y) + Width/Height
        # Rectangle expects: Center X, Center Y, Half-Width, Half-Height
        center_x = x + (w / 2)
        center_y = y + (h / 2)
        half_w = w / 2
        half_h = h / 2
        
        search_boundary = Rectangle(center_x, center_y, half_w, half_h)
        
        qt.query(search_boundary, found)
        
        return jsonify([{"x": p.x, "y": p.y, **p.data} for p in found])

    except Exception as e:
        print(f"❌ CRASH: {e}")
        return jsonify({"error": str(e)}), 500

# --- NEW: VISUALIZER ENDPOINT ---
@app.route('/grid', methods=['GET'])
def get_grid():
    """Returns the visual boundaries of the Quadtree nodes"""
    boxes = []
    
    def traverse(node):
        # Convert Center/Half-Width to Top-Left/Width/Height for Canvas
        boxes.append({
            "x": node.boundary.x - node.boundary.w,
            "y": node.boundary.y - node.boundary.h,
            "w": node.boundary.w * 2,
            "h": node.boundary.h * 2
        })
        if node.divided:
            traverse(node.ne)
            traverse(node.nw)
            traverse(node.se)
            traverse(node.sw)
            
    traverse(qt)
    return jsonify(boxes)

if __name__ == '__main__': 
    app.run(debug=True, port=5000)