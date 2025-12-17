import os
import random

# 1. Define the descriptive words to generate random titles
ADJECTIVES = ["Cozy", "Modern", "Luxury", "Spacious", "Affordable", "Sunny", "Private", "Charming", "Urban", "Secluded"]
TYPES = ["Studio", "Loft", "Apartment", "Condo", "Suite", "Penthouse", "Room", "Bungalow", "Villa", "Cabin"]
LOCATIONS = ["Downtown", "near Park", "with View", "in Suburbs", "near Metro", "uptown", "by the Lake", "in Historic District"]

# 2. Setup the folder path
base_folder = "fakeimages"
if not os.path.exists(base_folder):
    os.makedirs(base_folder)

# 3. Start generating the Python file content
py_content = "LISTING_TEMPLATES = [\n"

print(f"🚀 Generating folders in '{base_folder}'...")

for i in range(1, 101): # Generate 100 listings
    # Create a unique folder name: listing_1, listing_2, ...
    folder_name = f"listing_{i}"
    full_path = os.path.join(base_folder, folder_name)
    
    # Create the actual folder on your computer
    if not os.path.exists(full_path):
        os.makedirs(full_path)
    
    # Generate random data
    price = f"${random.randint(800, 5000):,}"
    title = f"{random.choice(ADJECTIVES)} {random.choice(TYPES)} {random.choice(LOCATIONS)}"
    
    # The 'img' field points to a 'cover.jpg' inside that specific folder
    # You will need to put a real image named 'cover.jpg' in there later!
    img_path = f"{folder_name}/cover.jpg"
    
    # Add to the Python list string
    py_content += f'    {{ "price": "{price}", "title": "{title}", "img": "{img_path}" }},\n'

py_content += "]\n"

# 4. Save this data to a new file called 'listings_data.py'
with open("listings_data.py", "w", encoding="utf-8") as f:
    f.write(py_content)

print("✅ Done! Created 100 folders and 'listings_data.py'.")
print("👉 You can now import LISTING_TEMPLATES from listings_data in your server.py")