🗺️ Geospatial Searcher - Data Structures Project

This is the central README for our project. If you are lost, start here.

Project Deadline: 12/11/2025

👥 Our Team

Team 1 (Back-End / Python): Eni, Bato

Team 2 (Front-End / JS): Dan, Laila

🗓️ Important Dates

Project Start: 2025-11-15

Front-End v2 (Gallery) Complete: 2025-11-17

Back-End (Quadtree) Target Date:

Full Integration Target Date:

Final Presentation: 

# How to Run This Project (Quick Start)

The project is in two parts. You must run both to see the final version.

1. Back-End (Team 1)

This runs the Python server and the "fast" Quadtree search.

Make sure you have the latest code: git pull

Install the required packages (only need to do this once):

py -m pip install -r requirements.txt


Run the server:

py server.py


Leave this terminal open. The server is now running at http://127.0.0.1:5000.

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

Front-End: 90% complete. The UI is built and works perfectly in "Slow Mode."

Back-End: 25% complete. The server runs, but the quadtree.py logic is empty.

Integration: The two parts are NOT connected yet.

🟢 TASKS DONE (Completed)

[X] Setup GitHub repository (Alex)

[X] Fix Python/Flask installation issues (Alex)

[X] Create all foundation files for Front-End and Back-End (Alex)

[X] (Front-End) Add custom map image background (Alex)

[X] (Front-End) Implement "Listing Template" system (Alex)

[X] (Front-End) Build sidebar UI to show found listings (Alex)

[X] (Front-End) Build pop-up image gallery modal (Alex)

[X] (Front-End) Create 58 fake listing templates (Alex)

🔴 TO-DO: Team 1 (Eni & Bato) - Back-End

This is our #1 priority. We must finish the data structure.

[ ] Implement quadtree.py:

[ ] Open quadtree.py.

[ ] Follow the "TASK" comments to fill in the logic for divide().

[ ] Follow the "TASK" comments to fill in the logic for insert().

[ ] Follow the "TASK" comments to fill in the logic for query() (the most important one).

[ ] Update server.py:

[ ] The server is generating random points right now. We need to copy the LISTING_TEMPLATES array from script.js into server.py so the server has the same rich data.

[ ] Update the generateRandomPoints function in server.py to use these templates (just like script.js does).

[ ] Update the /search function. Right now, it sends back [{x, y}, ...]. It needs to send back the full point object (title, price, photos, etc.) so the sidebar can be built.

[ ] Test:

[ ] Test your /search endpoint (using a tool like Postman, or just ask Alex) to make sure it returns the correct list of full listing objects.

🟡 TO-DO: Team 2 (Dan & Laila) - Front-End

Your "slow mode" is working, but your final job is to connect to Team 1.

[ ] Understand the new code:

[ ] Run git pull!

[ ] Open index.html, style.css, and script.js and see how the new sidebar and image gallery work.

[ ] Polish:

[ ] Feel free to improve style.css. Change colors, fonts, or alignments.

[ ] Add more real images to the fakeimages folder and update the LISTING_TEMPLATES array in script.js. (Make sure to tell Team 1, so they can copy the new array to server.py!)

[ ] Final Integration (Waiting on Team 1):

[ ] This is the last and most important step.

[ ] Go to script.js and find the mouseup function.

[ ] Delete the "Slow Search" loop.

[ ] Implement the "Fast Search" by adding the fetch() command to call Team 1's server (http://127.0.0.1:5000/search).

[ ] Get the list of results from the server and pass it to foundPoints.

[ ] Test the complete, live-data application.

🔵 TO-DO: Project Manager (Alex)

[ ] Make sure everyone can run the project and understands their tasks.

[ ] Help Team 1 test their back-end.

[ ] Coordinate the "Final Integration" step between both teams.

[ ] Prepare the final presentation slides.