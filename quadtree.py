# quadtree.py
# This is Team 1's file. You will build the Quadtree logic here.

from helpers import Point, Rectangle

class Quadtree:
    def __init__(self, boundary, capacity):
        self.boundary = boundary # A Rectangle object
        self.capacity = capacity   # Max number of points before dividing
        self.points = []         # A list to store the Point objects
        self.divided = False     # A boolean to check if this has subdivided

    def divide(self):
        """
        TASK FOR TEAM 1:
        1. Calculate the new dimensions for four child quadrants.
           (e.g., half the width and half the height of self.boundary)
        2. Create four new Rectangle objects for these new quadrants.
        3. Create four new Quadtree objects (self.northwest, self.northeast, etc.)
           using these new boundaries and the same capacity.
        4. Set self.divided = True
        """
        # --- TEAM 1: WRITE YOUR CODE HERE ---
        pass
        # --- END OF TEAM 1 CODE ---

    def insert(self, point):
        """
        TASK FOR TEAM 1:
        This function will add a point to the quadtree.
        
        1. Check if the point is inside this quadtree's `self.boundary`.
           (Use the `self.boundary.contains(point)` method). If not, return.
        
        2. If this tree is not full (i.e., len(self.points) < self.capacity):
           Add the point to the `self.points` list.
        
        3. If this tree IS full:
           a. If it's not already `self.divided`, call `self.divide()`.
           b. Insert this point into the correct child (NW, NE, SW, SE).
              (You'll need to check which child's boundary contains the point).
        """
        # --- TEAM 1: WRITE YOUR CODE HERE ---
        pass
        # --- END OF TEAM 1 CODE ---


    def query(self, search_range):
        """
        TASK FOR TEAM 1:
        This function will find all points inside a given range.
        
        1. Create an empty list `found_points = []`.
        
        2. Check if the `search_range` (a Rectangle) overlaps with `self.boundary`.
           (Use the `self.boundary.intersects(search_range)` method).
           If not, return the empty list `found_points`.

        3. If it does overlap, check all points in `self.points`.
           For each point, check if the `search_range.contains(point)`.
           If yes, add it to `found_points`.

        4. If `self.divided` is True:
           Recursively call `query` on all four children (e.g., self.northwest.query(...))
           and add their results to your `found_points` list.
        
        5. Return `found_points`.
        """
        # --- TEAM 1: WRITE YOUR CODE HERE ---
        return [] # Return an empty list for now
        # --- END OF TEAM 1 CODE ---