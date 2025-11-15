# main.py
# This is Team 2's file. It runs the visual part of the app.
# This file ALREADY WORKS in "Slow Mode".

import pygame
import random
from helpers import Point, Rectangle
# We will import Team 1's work later
# from quadtree import Quadtree 

# --- Settings ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
POINT_COUNT = 2000          # Number of random points
POINT_COLOR = (255, 255, 255) # White
FOUND_COLOR = (0, 255, 0)     # Green
BOX_COLOR = (0, 150, 255)     # Blue
BG_COLOR = (20, 20, 20)       # Dark grey

# --- Data Generation ---
def generate_random_points(count, width, height):
    """Creates a list of random Point objects."""
    points = []
    for _ in range(count):
        x = random.randint(0, width)
        y = random.randint(0, height)
        points.append(Point(x, y))
    return points

# --- Main Application ---
def main():
    # Pygame setup
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Geospatial Searcher (Slow Mode)")
    clock = pygame.time.Clock()

    # Generate our master list of points
    all_points = generate_random_points(POINT_COUNT, SCREEN_WIDTH, SCREEN_HEIGHT)

    # Variables for mouse dragging
    found_points = []
    is_dragging = False
    drag_start_pos = (0, 0)
    search_rect_obj = None # This will be our search Rectangle

    running = True
    while running:
        # --- Event Handling ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                is_dragging = True
                drag_start_pos = event.pos
                found_points = [] # Clear old results
                search_rect_obj = None

            elif event.type == pygame.MOUSEBUTTONUP:
                is_dragging = False
                # Create the final Rectangle object for searching
                x1, y1 = drag_start_pos
                x2, y2 = event.pos
                
                # Normalize the rectangle (top-left x,y and positive w,h)
                search_x = min(x1, x2)
                search_y = min(y1, y2)
                search_w = abs(x1 - x2)
                search_h = abs(y1 - y2)
                
                if search_w > 0 and search_h > 0:
                    search_rect_obj = Rectangle(search_x, search_y, search_w, search_h)

                    # --- THIS IS THE "SLOW" SEARCH ---
                    # Team 2: When Team 1 is done, you will replace this
                    # "for" loop with a call to the Quadtree's "query" function.
                    print("Running slow search...")
                    found_points = []
                    for point in all_points:
                        if search_rect_obj.contains(point):
                            found_points.append(point)
                    print(f"Found {len(found_points)} points.")
                    # --- END OF SLOW SEARCH ---

            elif event.type == pygame.MOUSEMOTION and is_dragging:
                pass # The box is drawn in the "Drawing" section

        # --- Drawing ---
        screen.fill(BG_COLOR)

        # 1. Draw all points (as small white dots)
        for point in all_points:
            pygame.draw.circle(screen, POINT_COLOR, (point.x, point.y), 2)

        # 2. Draw the found points (as larger green dots)
        for point in found_points:
            pygame.draw.circle(screen, FOUND_COLOR, (point.x, point.y), 3)

        # 3. Draw the drag box
        if is_dragging:
            x1, y1 = drag_start_pos
            x2, y2 = pygame.mouse.get_pos()
            # Draw the blue rectangle
            pygame.draw.rect(screen, BOX_COLOR, (min(x1,x2), min(y1,y2), abs(x1-x2), abs(y1-y2)), 2)

        # --- Update Display ---
        pygame.display.flip()
        clock.tick(60) # Run at 60 FPS

    pygame.quit()

# This is the standard way to run a Python program
if __name__ == "__main__":
    main()