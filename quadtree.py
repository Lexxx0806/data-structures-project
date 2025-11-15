# quadtree.py
# This is Team 1's main file. You will build the Quadtree logic here.

from helpers import Point, Rectangle

class Quadtree:
    def __init__(self, boundary, capacity):
        self.boundary = boundary # A Rectangle object
        self.capacity = capacity   # Max number of points before dividing
        self.points = []         # A list to store the Point objects
        self.divided = False     # A boolean to check if this has subdivided

    def divide(self):
        """
        TASK FOR TEAM 1 (Step 1): Implement the divide function.
        
        This function should create four new "child" Quadtrees.
        """
        
        # 1. Get the x, y, width, and height from our current boundary
        x = self.boundary.x
        y = self.boundary.y
        half_w = self.boundary.width / 2
        half_h = self.boundary.height / 2

        # 2. Create four new Rectangle objects for the quadrants
        #    (e.g., nw_boundary = Rectangle(x, y, half_w, half_h))
        nw_boundary = Rectangle(x, y, half_w, half_h)
        ne_boundary = Rectangle(x + half_w, y, half_w, half_h)
        sw_boundary = Rectangle(x, y + half_h, half_w, half_h)
        se_boundary = Rectangle(x + half_w, y + half_h, half_w, half_h)

        # 3. Create the four new Quadtree "child" objects
        #    (Use `self.capacity` as the capacity for the new trees)
        self.northwest = Quadtree(nw_boundary, self.capacity)
        self.northeast = Quadtree(ne_boundary, self.capacity)
        self.southwest = Quadtree(sw_boundary, self.capacity)
        self.southeast = Quadtree(se_boundary, self.capacity)

        # 4. Set our `divided` flag to True
        self.divided = True

    def insert(self, point):
        """
        TASK FOR TEAM 1 (Step 2): Implement the insert function.
        
        This function adds a point to the quadtree.
        """
        
        # 1. Check if the point is inside this quadtree's `self.boundary`.
        #    Use the `self.boundary.contains(point)` method.
        #    If it's not, just `return` (stop the function).
        if not self.boundary.contains(point):
            return

        # 2. If this tree is not full (i.e., len(self.points) < self.capacity):
        #    Add the point to the `self.points` list.
        #    Then, `return` (stop the function).
        if len(self.points) < self.capacity:
            self.points.append(point)
            return

        # 3. If this tree IS full and not yet divided:
        #    Call `self.divide()` to create the child quadrants.
        if not self.divided:
            self.divide()

        # 4. We are now full AND divided.
        #    Try to insert the point into the correct child.
        #    (The child's `insert` function will do its own checks).
        if self.northeast.insert(point):
            return
        elif self.northwest.insert(point):
            return
        elif self.southeast.insert(point):
            return
        elif self.southwest.insert(point):
            return

    def query(self, search_range):
        """
        TASK FOR TEAM 1 (Step 3): Implement the query function.
        
        This finds all points inside a given `search_range` (a Rectangle).
        """
        
        # 1. Create an empty list to hold the points we find.
        found_points = []

        # 2. Check if the `search_range` overlaps with `self.boundary`.
        #    Use the `self.boundary.intersects(search_range)` method.
        #    If not, `return` the empty `found_points` list.
        if not self.boundary.intersects(search_range):
            return found_points

        # 3. If it does overlap, check all points in `self.points`.
        #    For each point, check if the `search_range.contains(point)`.
        #    If yes, add it to `found_points`.
        for point in self.points:
            if search_range.contains(point):
                found_points.append(point)

        # 4. If `self.divided` is True:
        #    Recursively call `query` on all four children.
        #    Add the results from each child to your `found_points` list.
        #    (e.g., `found_points.extend(self.northwest.query(search_range))`)
        if self.divided:
            found_points.extend(self.northwest.query(search_range))
            found_points.extend(self.northeast.query(search_range))