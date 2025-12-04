# server.py
# Back-End: Now generates RICH data matching the Front-End

from flask import Flask, request, jsonify
from flask_cors import CORS
import random

from helpers import Point, Rectangle
from quadtree import Quadtree 

# --- Settings ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
POINT_COUNT = 100 # You set this to 100

# --- Flask Server Setup ---
app = Flask(__name__)
CORS(app) 

# --- NEW: LISTING TEMPLATES (MOVED TO TOP) ---
# Python needs to see these BEFORE it runs the code below.
LISTING_TEMPLATES = [
    {
        "title": "Cozy Studio near YZU",
        "type": "Studio",
        "address": "123 Yongfu Rd, Zhongli",
        "price": 8500,
        "photos": [
            'fakeimages/fakeroom1.jpg', 
            'fakeimages/fakeroom1.1.jpg',
            'fakeimages/fakeroom1.2.jpg',
            'fakeimages/fakeroom1.3.jpg',
            'fakeimages/fakeroom1.4.jpg'
        ]
    },
    {
        "title": "Modern 1-BR Apartment",
        "type": "1-BR Apartment",
        "address": "456 Luguang Rd, Zhongli",
        "price": 14000,
        "photos": ['fakeimages/room2_a.jpg', 'fakeimages/room2_b.jpg']
    },
    {
        "title": "Spacious Family Home",
        "type": "3-BR Home",
        "address": "789 Rongmin Rd, Zhongli",
        "price": 26000,
        "photos": ['fakeimages/room3_a.jpg']
    },
    {
        "title": "Bright Studio by the Park",
        "type": "Studio",
        "address": "50 Xinxing Rd, Zhongli",
        "price": 9500,
        "photos": ['fakeimages/room4_a.jpg', 'fakeimages/room4_b.jpg']
    },
    {
        "title": "Simple Room (Shared Bath)",
        "type": "Room",
        "address": "21 Huanzhong Rd, Zhongli",
        "price": 5500,
        "photos": ['fakeimages/room5_a.jpg']
    },
    {
        "title": "Renovated 2-BR",
        "type": "2-BR Apartment",
        "address": "33 Huamei 1st Rd, Zhongli",
        "price": 18000,
        "photos": ['fakeimages/room6_a.jpg', 'fakeimages/room6_b.jpg', 'fakeimages/room6_c.jpg']
    },
    {
        "title": "Luxury Loft",
        "type": "Loft",
        "address": "88 Guangfu Rd, Zhongli",
        "price": 27500,
        "photos": ['fakeimages/room7_a.jpg', 'fakeimages/room7_b.jpg']
    },
    {
        "title": "Affordable Single Room",
        "type": "Room",
        "address": "112 Fuhua St, Zhongli",
        "price": 6000,
        "photos": ['fakeimages/room8_a.jpg']
    },
    # --- 50 NEW TEMPLATES ---
    {
        "title": "Sunny 1-BR near Dazhentou",
        "type": "1-BR Apartment",
        "address": "45 Jixian Rd, Zhongli",
        "price": 13500,
        "photos": ['fakeimages/room9_a.jpg', 'fakeimages/room9_b.jpg']
    },
    {
        "title": "Quiet Room for Students",
        "type": "Room",
        "address": "220 Zhongbei Rd, Zhongli",
        "price": 7000,
        "photos": ['fakeimages/room10_a.jpg']
    },
    {
        "title": "2-BR w/ Balcony",
        "type": "2-BR Apartment",
        "address": "77 Puzhong Rd, Zhongli",
        "price": 16500,
        "photos": ['fakeimages/room11_a.jpg', 'fakeimages/room11_b.jpg']
    },
    {
        "title": "Studio near Zhongli Station",
        "type": "Studio",
        "address": "19 Jianxing Rd, Zhongli",
        "price": 10000,
        "photos": ['fakeimages/room12_a.jpg']
    },
    {
        "title": "Large 4-BR House",
        "type": "4-BR Home",
        "address": "30 Lane 725, Jiadong Rd",
        "price": 28000,
        "photos": ['fakeimages/room13_a.jpg', 'fakeimages/room13_b.jpg']
    },
    {
        "title": "Penthouse Loft",
        "type": "Loft",
        "address": "500 Minzu Rd, Zhongli",
        "price": 27000,
        "photos": ['fakeimages/room14_a.jpg']
    },
    {
        "title": "Basic Room, All Utilities Incl.",
        "type": "Room",
        "address": "88 Zhongmei Rd, Zhongli",
        "price": 6500,
        "photos": ['fakeimages/room15_a.jpg']
    },
    {
        "title": "New 1-BR Condo",
        "type": "1-BR Apartment",
        "address": "12 Long'an St, Zhongli",
        "price": 15000,
        "photos": ['fakeimages/room16_a.jpg', 'fakeimages/room16_b.jpg']
    },
    {
        "title": "YZU Student Dorm (Private)",
        "type": "Room",
        "address": "55 Wenhua 2nd Rd, Zhongli",
        "price": 7200,
        "photos": ['fakeimages/room17_a.jpg']
    },
    {
        "title": "2-BR near Xinjin Park",
        "type": "2-BR Apartment",
        "address": "210 Xinxing Rd, Zhongli",
        "price": 17000,
        "photos": ['fakeimages/room18_a.jpg']
    },
    {
        "title": "Studio (Newly Furnished)",
        "type": "Studio",
        "address": "90 Longgang Rd, Zhongli",
        "price": 11000,
        "photos": ['fakeimages/room19_a.jpg']
    },
    {
        "title": "Small Studio",
        "type": "Studio",
        "address": "13 Huanbei Rd, Zhongli",
        "price": 8000,
        "photos": ['fakeimages/room20_a.jpg']
    },
    {
        "title": "3-BR for Family or Shares",
        "type": "3-BR Home",
        "address": "25 Yixing Rd, Zhongli",
        "price": 22000,
        "photos": ['fakeimages/room1_b.jpg', 'fakeimages/room3_a.jpg']
    },
    {
        "title": "Minimalist Room",
        "type": "Room",
        "address": "300 Zhongshan Rd, Zhongli",
        "price": 5000,
        "photos": ['fakeimages/room2_b.jpg']
    },
    {
        "title": "Loft near Luguang",
        "type": "Loft",
        "address": "44 Zhongxiao Rd, Zhongli",
        "price": 21000,
        "photos": ['fakeimages/room4_a.jpg']
    },
    {
        "title": "1-BR with City View",
        "type": "1-BR Apartment",
        "address": "99 Jianguo Rd, Zhongli",
        "price": 14500,
        "photos": ['fakeimages/room5_a.jpg']
    },
    {
        "title": "Studio near Night Market",
        "type": "Studio",
        "address": "12 Mingde Rd, Zhongli",
        "price": 9000,
        "photos": ['fakeimages/room6_b.jpg']
    },
    {
        "title": "Large Room in Shared Apt",
        "type": "Room",
        "address": "34 Wuquan Rd, Zhongli",
        "price": 7500,
        "photos": ['fakeimages/room7_b.jpg']
    },
    {
        "title": "2-BR, Pet Friendly",
        "type": "2-BR Apartment",
        "address": "58 Yumin St, Zhongli",
        "price": 19000,
        "photos": ['fakeimages/room8_a.jpg', 'fakeimages/room9_a.jpg']
    },
    {
        "title": "Single Room, Female Only",
        "type": "Room",
        "address": "70 Wenhua Rd, Zhongli",
        "price": 6200,
        "photos": ['fakeimages/room10_a.jpg']
    },
    {
        "title": "Studio, Top Floor",
        "type": "Studio",
        "address": "22 Yongle Rd, Zhongli",
        "price": 10500,
        "photos": ['fakeimages/room11_b.jpg']
    },
    {
        "title": "Massive 3-BR Condo",
        "type": "3-BR Home",
        "address": "150 Zhongzheng Rd, Zhongli",
        "price": 27500,
        "photos": ['fakeimages/room12_a.jpg']
    },
    {
        "title": "Economic Room",
        "type": "Room",
        "address": "43 Chang'an St, Zhongli",
        "price": 5000,
        "photos": ['fakeimages/room13_b.jpg']
    },
    {
        "title": "1-BR with Kitchen",
        "type": "1-BR Apartment",
        "address": "18 Longdong Rd, Zhongli",
        "price": 13000,
        "photos": ['fakeimages/room14_a.jpg']
    },
    {
        "title": "Studio+Balcony",
        "type": "Studio",
        "address": "66 Sanyuan Rd, Zhongli",
        "price": 11500,
        "photos": ['fakeimages/room15_a.jpg']
    },
    {
        "title": "Shared Apartment",
        "type": "Room",
        "address": "9 Longci Rd, Zhongli",
        "price": 6800,
        "photos": ['fakeimages/room16_b.jpg']
    },
    {
        "title": "2-BR near Ring Rd",
        "type": "2-BR Apartment",
        "address": "140 Huanxi Rd, Zhongli",
        "price": 17500,
        "photos": ['fakeimages/room17_a.jpg']
    },
    {
        "title": "New Building Studio",
        "type": "Studio",
        "address": "200 Minquan Rd, Zhongli",
        "price": 12000,
        "photos": ['fakeimages/room18_a.jpg']
    },
    {
        "title": "3-BR near Zhongli Arts Hall",
        "type": "3-BR Home",
        "address": "100 Zhonghe Rd, Zhongli",
        "price": 24000,
        "photos": ['fakeimages/room19_a.jpg']
    },
    {
        "title": "Simple Studio",
        "type": "Studio",
        "address": "35 Yanping Rd, Zhongli",
        "price": 8800,
        "photos": ['fakeimages/room20_a.jpg']
    },
    {
        "title": "1-BR near Jungli Train Station",
        "type": "1-BR Apartment",
        "address": "55 Zhonghe Rd, Zhongli",
        "price": 13000,
        "photos": ['fakeimages/room1_c.jpg']
    },
    {
        "title": "Room with Private Bath",
        "type": "Room",
        "address": "80 Zhongxiao Rd, Zhongli",
        "price": 7800,
        "photos": ['fakeimages/room2_a.jpg']
    },
    {
        "title": "2-BR in Luguang Village",
        "type": "2-BR Apartment",
        "address": "12 Luguang Rd, Zhongli",
        "price": 15500,
        "photos": ['fakeimages/room3_a.jpg']
    },
    {
        "title": "Studio with a View",
        "type": "Studio",
        "address": "210 Fuhua St, Zhongli",
        "price": 10000,
        "photos": ['fakeimages/room4_b.jpg']
    },
    {
        "title": "Cheapest Room in Town",
        "type": "Room",
        "address": "5 Jiadong Rd, Zhongli",
        "price": 5000,
        "photos": ['fakeimages/room5_a.jpg']
    },
    {
        "title": "Modern 2-BR",
        "type": "2-BR Apartment",
        "address": "66 Rongmin Rd, Zhongli",
        "price": 19000,
        "photos": ['fakeimages/room6_c.jpg']
    },
    {
        "title": "YZU Area Studio",
        "type": "Studio",
        "address": "30 Lane 123, Yongfu Rd",
        "price": 9200,
        "photos": ['fakeimages/room7_a.jpg']
    },
    {
        "title": "1-BR, Fully Furnished",
        "type": "1-BR Apartment",
        "address": "45 Xinxing Rd, Zhongli",
        "price": 14200,
        "photos": ['fakeimages/room8_a.jpg']
    },
    {
        "title": "Large Room",
        "type": "Room",
        "address": "180 Huanzhong Rd, Zhongli",
        "price": 7300,
        "photos": ['fakeimages/room9_b.jpg']
    },
    {
        "title": "3-BR near YZU",
        "type": "3-BR Home",
        "address": "55 Wenhua 2nd Rd, Zhongli",
        "price": 23000,
        "photos": ['fakeimages/room10_a.jpg']
    },
    {
        "title": "Studio w/ Kitchenette",
        "type": "Studio",
        "address": "77 Puzhong Rd, Zhongli",
        "price": 10800,
        "photos": ['fakeimages/room11_a.jpg']
    },
    {
        "title": "2-BR near Xinjin",
        "type": "2-BR Apartment",
        "address": "250 Xinxing Rd, Zhongli",
        "price": 16000,
        "photos": ['fakeimages/room12_a.jpg']
    },
    {
        "title": "Shared Room, Low Price",
        "type": "Room",
        "address": "33 Huamei 1st Rd, Zhongli",
        "price": 5200,
        "photos": ['fakeimages/room13_a.jpg']
    },
    {
        "title": "1-BR by Park",
        "type": "1-BR Apartment",
        "address": "80 Guangfu Rd, Zhongli",
        "price": 13800,
        "photos": ['fakeimages/room14_a.jpg']
    },
    {
        "title": "Studio (All Inclusive)",
        "type": "Studio",
        "address": "42 Fuhua St, Zhongli",
        "price": 11000,
        "photos": ['fakeimages/room15_a.jpg']
    },
    {
        "title": "Room in Quiet Area",
        "type": "Room",
        "address": "10 Lane 725, Jiadong Rd",
        "price": 5800,
        "photos": ['fakeimages/room16_a.jpg']
    },
    {
        "title": "2-BR Condo, New Bldg",
        "type": "2-BR Apartment",
        "address": "300 Minzu Rd, Zhongli",
        "price": 21000,
        "photos": ['fakeimages/room17_a.jpg']
    },
    {
        "title": "Bright Studio",
        "type": "Studio",
        "address": "15 Jianxing Rd, Zhongli",
        "price": 9000,
        "photos": ['fakeimages/room18_a.jpg']
    },
    {
        "title": "3-BR (Pets OK)",
        "type": "3-BR Home",
        "address": "70 Long'an St, Zhongli",
        "price": 24500,
        "photos": ['fakeimages/room19_a.jpg']
    },
    {
        "title": "Small Room",
        "type": "Room",
        "address": "50 Zhongbei Rd, Zhongli",
        "price": 5300,
        "photos": ['fakeimages/room20_a.jpg']
    }
]

# --- Global Quadtree ---
world_boundary = Rectangle(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
qtree = Quadtree(world_boundary, 4)

# --- Generate Data ---
print(f"Generating and inserting {POINT_COUNT} points...")
for i in range(POINT_COUNT):
    # 1. Pick a random template
    template = random.choice(LISTING_TEMPLATES)
    
    x = random.randint(0, SCREEN_WIDTH)
    y = random.randint(0, SCREEN_HEIGHT)
    
    # 2. Create the Point object
    p = Point(x, y)
    
    # 3. Attach the RICH DATA to the point
    p.id = f"listing-{i}"
    p.title = template["title"]
    p.type = template["type"]
    p.address = template["address"]
    p.price = template["price"]
    p.photos = template["photos"]
    
    # 4. Insert into Quadtree
    qtree.insert(p)
    
print("...Done. Server is ready.")


# --- API Endpoint ---
@app.route('/search', methods=['POST'])
def search_quadtree():
    data = request.json
    
    # Basic validation to prevent crashes
    if not data or 'x' not in data:
        return jsonify([])

    search_box = Rectangle(
        data['x'],
        data['y'],
        data['width'],
        data['height']
    )
    
    found_points = qtree.query(search_box)
    
    # --- SEND RICH DATA BACK ---
    # We must convert the Point objects into a JSON dictionary
    results = []
    for p in found_points:
        results.append({
            'id': getattr(p, 'id', 'unknown'),
            'x': p.x, 
            'y': p.y,
            # Use getattr to avoid crashes if data is missing
            'title': getattr(p, 'title', 'Unknown Title'),
            'type': getattr(p, 'type', 'Unknown Type'),
            'address': getattr(p, 'address', 'Unknown Address'),
            'price': getattr(p, 'price', 0),
            'photos': getattr(p, 'photos', [])
        })

    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True, port=5000)