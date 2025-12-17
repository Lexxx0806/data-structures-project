# This is for server.py
from flask import Flask, jsonify, request
from flask_cors import CORS
import random
from helpers import Point, Rectangle
from quadtree import Quadtree

app = Flask(__name__)
CORS(app)

# 5 Photos per template
LISTING_TEMPLATES = [
    {
        "type": "Studio", "title": "Modern Downtown Studio", "base_price": 1200,
        "photos": ["https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?w=600","https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=600","https://images.unsplash.com/photo-1584622050111-993a426fbf0a?w=600","https://images.unsplash.com/photo-1556911220-e15b29be8c8f?w=600","https://images.unsplash.com/photo-1497366216548-37526070297c?w=600"]
    },
    {
        "type": "Loft", "title": "Industrial Loft with View", "base_price": 2400,
        "photos": ["https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=600","https://images.unsplash.com/photo-1534349767944-1e244d2d1ab1?w=600","https://images.unsplash.com/photo-1512917774080-9991f1c4c750?w=600","https://images.unsplash.com/photo-1505691938271-e734b5c0f6a9?w=600","https://images.unsplash.com/photo-1513519245088-0e12902e5a38?w=600"]
    },
    {
        "type": "Apartment", "title": "Cozy 1-Bedroom Apartment", "base_price": 1800,
        "photos": ["https://images.unsplash.com/photo-1493809842364-78817add7ffb?w=600","https://images.unsplash.com/photo-1502005229762-cf1b2da7c5d6?w=600","https://images.unsplash.com/photo-1484154218962-a1c002085d2f?w=600","https://images.unsplash.com/photo-1560448204-603b3fc33ddc?w=600","https://images.unsplash.com/photo-1560185007-c5ca9d2c014d?w=600"]
    },
    {
        "type": "Penthouse", "title": "Luxury Penthouse Suite", "base_price": 4500,
        "photos": ["https://images.unsplash.com/photo-1512917774080-9991f1c4c750?w=600","https://images.unsplash.com/photo-1616594039964-40832456ba15?w=600","https://images.unsplash.com/photo-1556911220-e15b29be8c8f?w=600","https://images.unsplash.com/photo-1477959858617-67f85cf4f1df?w=600","https://images.unsplash.com/photo-1584622050111-993a426fbf0a?w=600"]
    },
    {
        "type": "House", "title": "Suburban Family Home", "base_price": 3200,
        "photos": ["https://images.unsplash.com/photo-1564013799919-ab600027ffc6?w=600","https://images.unsplash.com/photo-1484154218962-a1c002085d2f?w=600","https://images.unsplash.com/photo-1595295333158-4742f28fbd85?w=600","https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=600","https://images.unsplash.com/photo-1617806118233-18e1de247200?w=600"]
    },
    {
        "type": "Condo", "title": "Bright High-Rise Condo", "base_price": 2100,
        "photos": ["https://images.unsplash.com/photo-1494526585095-c41746248156?w=600","https://images.unsplash.com/photo-1556020685-ae41abfc9365?w=600","https://images.unsplash.com/photo-1512915922686-57c11dde9b6b?w=600","https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=600","https://images.unsplash.com/photo-1565514020176-db79238b6d88?w=600"]
    }
]

STREETS = ["Main St", "Broadway", "Park Ave", "Oak Ln", "Pine St", "Maple Dr", "Cedar Rd", "Sunset Blvd", "River Rd"]
boundary = Rectangle(400, 300, 400, 300)
qt = Quadtree(boundary, 4)

print("🌳 Generating 200 random listings...")
for i in range(200):
    x, y = random.randint(0, 800), random.randint(0, 600)
    tmpl = random.choice(LISTING_TEMPLATES)
    data = { "id": i, "title": tmpl["title"], "type": tmpl["type"], "price": tmpl["base_price"] + random.choice([0,50,-50,100]), "address": f"{random.randint(10,999)} {random.choice(STREETS)}", "photos": tmpl["photos"] }
    qt.insert(Point(x, y, data))
print("✅ Quadtree built!")

@app.route('/')
def home(): return "Server is running! Use /search endpoint."

@app.route('/search', methods=['POST'])
def search():
    try:
        # 1. READ DATA SAFELY
        data = request.get_json(force=True, silent=True)
        
        # 2. LOGGING (So you can see what is happening in the terminal)
        if not data:
            print("⚠️ Request received with NO DATA.")
            return jsonify({"error": "No data"}), 400
        
        # 3. EXTRACTION with FALLBACKS (Handles 'w' OR 'width')
        raw_x = data.get('x')
        raw_y = data.get('y')
        raw_w = data.get('w') if 'w' in data else data.get('width')
        raw_h = data.get('h') if 'h' in data else data.get('height')

        # 4. SAFETY CHECK (Prevents the crash)
        if raw_x is None or raw_y is None or raw_w is None or raw_h is None:
            print(f"❌ Error: Missing fields. Received: {data}")
            return jsonify({"error": "Missing parameters x,y,w,h"}), 400

        # 5. CONVERSION
        x, y, w, h = float(raw_x), float(raw_y), float(raw_w), float(raw_h)

        # 6. SEARCH
        found = []
        qt.query(Rectangle(x+(w/2), y+(h/2), w/2, h/2), found)
        return jsonify([{"x": p.x, "y": p.y, **p.data} for p in found])

    except Exception as e:
        print(f"❌ CRASH: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__': app.run(debug=True, port=5000)