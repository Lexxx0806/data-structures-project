🗺️ Geospatial Searcher - Data Structures Project

This is the central README for our project. If you are lost, start here.

Project Deadline: 12/17/2025

🎯 Project Goal

The primary objective of this project is to demonstrate the efficiency of the Quadtree data structure in a real-world application.

We are building a Geospatial Search Engine for rental listings. Instead of checking every single listing one by one (which is slow), we use a Quadtree to recursively divide the map and instantly locate points within a user's search area. This project combines a complex back-end algorithm with a polished, interactive front-end interface.

👥 Our Team

Team 1 (Back-End / Python): Eni, Bato

Team 2 (Front-End / JS): Dan, Laila

💡 How It Works (The Concept)

If you are confused about why we have two parts, think of our project like a Restaurant:

The Server (server.py) is the Kitchen: It runs in the background and waits for specific orders. It doesn't have a "menu" you can look at. Right now, it only knows how to respond to one specific command: /search. If you try to open it directly in a browser, it will give you a 404 error because you didn't give it an order!

The Website (index.html) is the Dining Room: This is the menu that customers actually look at. You open this file to see the interface. When you drag the mouse to search, the "Dining Room" secretly sends a message to the "Kitchen" to get the data.

🗓️ Important Dates

Project Start: 2025-11-15

Front-End v2 (Gallery) Complete: 2025-11-17

Back-End (Quadtree) Target Date: 2025-11-28

Full Integration Target Date: 2025-12-05

Final Presentation: 2025-12-11

🚀 How to Run This Project (Quick Start)

The project is in two parts. You must run both to see the final version.

1. Back-End (Team 1)

This runs the Python server and the "fast" Quadtree search.

Make sure you have the latest code: git pull

Install the required packages (only need to do this once):

py -m pip install -r requirements.txt

Run the server:

py server.py

Note: Do not click the link it gives you (it will show a 404). Just leave this terminal open.

2. Front-End (Team 2)

This runs the website you see in the browser.

Make sure you have the latest code: git pull

Find the index.html file in the project folder.

Double-click index.html to open it in your web browser.

NOTE: The front-end is currently in "Slow Mode". It does not talk to the server yet. It uses its own fake search to let us build the UI. The final step is to connect these two parts.

🛠️ Project Architecture

1. Back-End (The "Kitchen") - Team 1

server.py: The Flask server. Creates the /search API endpoint that waits for requests.

quadtree.py: The "Brain". This file contains the logic for the Quadtree data structure (the insert and query functions).

helpers.py: Defines the Point and Rectangle classes.

requirements.txt: Lists the Python packages we need (Flask, Flask-CORS).

2. Front-End (The "Dining Room") - Team 2

index.html: The website "skeleton." Contains the <canvas>, sidebar, and pop-up modal.

style.css: All the styles ("paint and furniture") that make it look good.

script.js: The "waiter." This file does all the interactive work:

Draws the map and dots.

Handles mouse clicks and drags.

Builds the sidebar cards.

Runs the pop-up image gallery.

fakeimages/: The folder where we store all our fake room photos.

✅ Project Status & To-Do List

🚧 Current Status (as of Nov 17)

Front-End: 95% complete. The UI (v4) has a map, sidebar, and image gallery.

Back-End: 25% complete. The server runs, but the data is simple (dots only) and quadtree.py logic is empty.

Integration: The two parts are NOT connected yet.

🟢 TASKS DONE (Completed)

[x] Setup GitHub repository

[x] Fix Python/Flask installation issues

[x] Create all foundation files for Front-End and Back-End

[x] (Front-End) Add custom map image background

[x] (Front-End) Implement "Listing Template" system

[x] (Front-End) Build sidebar UI to show found listings

[x] (Front-End) Build pop-up image gallery modal

[x] (Front-End) Create 58 fake listing templates

🔴 TO-DO: Team 1 (Eni & Bato) - Back-End

This is our #1 priority. We must finish the data structure.

Implement quadtree.py:

[ ] Open quadtree.py.

[ ] Follow the "TASK" comments to fill in the logic for divide().

[ ] Follow the "TASK" comments to fill in the logic for insert().

[ ] Follow the "TASK" comments to fill in the logic for query() (the most important one).

Update server.py:

[ ] The server is currently generating simple dots. We need to copy the LISTING_TEMPLATES array from script.js into server.py.

[ ] Update the generateRandomPoints function in server.py to use these templates.

[ ] Update the /search function to send back the full point object (title, price, photos) so the sidebar works.

Test:

[ ] Use Postman or a test script to ensure /search returns the correct data.

🟡 TO-DO: Team 2 (Dan & Laila) - Front-End

Your main job is to polish the UI and prepare for integration.

Polish & Improvements (Optional but Recommended):

[ ] Pointer Cursor: Make the mouse cursor change to a "pointer hand" when hovering over a green/found dot (in script.js).

[ ] Custom Scrollbar: Style the sidebar scrollbar to match the dark theme (in style.css).

[ ] Empty State: Add a friendly "No listings found" message/icon to the sidebar when the search returns 0 results (in script.js).

Final Integration (Waiting on Team 1):

[ ] Delete the "Slow Search" loop in script.js.

[ ] Implement the "Fast Search" using fetch() to call Team 1's server (http://127.0.0.1:5000/search).

[ ] Test the complete application.

🔵 TO-DO: Project Coordination

[ ] Make sure everyone can run the project and understands their tasks.

[ ] Help Team 1 test their back-end.

[ ] Coordinate the "Final Integration" step between both teams.

[ ] Prepare the final presentation slides.
