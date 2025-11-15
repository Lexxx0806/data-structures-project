# server.py
# This is Team 1's NEW main file.
# Run it with: python server.py

from flask import Flask, request, jsonify
from flask_cors import CORS
import random

from helpers import Point, Rectangle
from quadtree import Quadtree 

# --- Settings ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
POINT_COUNT = 2000

# --- Flask Server Setup ---
# 1. Initialize the Flask app
app = Flask(__name__)
# 2. This is CRITICAL. It allows our JS (on a different "domain")
#    to make requests to this Python server.
CORS(app) 

# --- Global Quadtree ---
# This code runs ONE TIME when the server starts.

# 1. Create the "world" boundary
world_boundary = Rectangle(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)

# 2. Create the main Quadtree object
#    (Capacity=4 means divide after 4 points are in a section)
qtree = Quadtree(world_boundary, 4)

# 3. Generate random points and insert them into the Quadtree
print(f"Generating and inserting {POINT_COUNT} random points...")
for _ in range(POINT_COUNT):
    x = random.randint(0, SCREEN_WIDTH)
    y = random.randint(0, SCREEN_HEIGHT)
    p = Point(x, y)
    
    # This calls the `insert` function Team 1 must build
    qtree.insert(p) 
    
print("...Done. Server is ready.")


# --- API Endpoint ---
# This is the "listener" that waits for requests from the JavaScript.
@app.route('/search', methods=['POST'])
def search_quadtree():
    """
    This function is called by Team 2's JavaScript.
    It receives the search box and returns the found points.
    """
    
    # 1. Get the search box data from the JavaScript request
    #    The `data` variable will look like:
    #    { "x": 50, "y": 60, "width": 100, "height": 80 }
    data = request.json
    
    # 2. Create a Rectangle object for the search
    search_box = Rectangle(
        data['x'],
        data['y'],
        data['width'],
        data['height']
    )
    
    # 3.
    # --- TASK FOR TEAM 1 (Step 4: Integration) ---
    # Call the `query` function you built to find the points.
    #
    
    # This line calls the `query` function Team 1 must build
    found_points = qtree.query(search_box) 
    
    #
    # --- END OF TASK ---
    #
    
    # 4. Convert the list of Point objects into a simple JSON list
    #    that JavaScript can understand.
    #    (e.g., [{'x': 10, 'y': 20}, {'x': 15, 'y': 25}, ...])
    results = []
    for p in found_points:
        results.append({'x': p.x, 'y': p.y})

    # 5. Send the JSON list back to the JavaScript
    return jsonify(results)

# --- Run the Server ---
if __name__ == "__main__":
    # This runs the Flask server on http://127.0.0.1:5000/
    # Team 1 can leave this running in their terminal.
    # `debug=True` means the server will auto-restart when you save changes.
    app.run(debug=True, port=5000)