from helpers import Point, Rectangle

class Quadtree:
    def __init__(self, boundary, capacity):
        self.boundary = boundary  # A Rectangle object
        self.capacity = capacity  # Max number of points before dividing
        self.points = []          # A list to store Point objects
        self.divided = False      # Has this node been subdivided?

    def divide(self):
        """
        Create four child Quadtrees representing subdivisions
        of the current boundary.
        """
        x = self.boundary.x
        y = self.boundary.y
        half_w = self.boundary.width / 2
        half_h = self.boundary.height / 2

        # Create four sub-rectangles
        nw = Rectangle(x, y, half_w, half_h)
        ne = Rectangle(x + half_w, y, half_w, half_h)
        sw = Rectangle(x, y + half_h, half_w, half_h)
        se = Rectangle(x + half_w, y + half_h, half_w, half_h)

        # Create Quadtrees for each quadrant
        self.northwest = Quadtree(nw, self.capacity)
        self.northeast = Quadtree(ne, self.capacity)
        self.southwest = Quadtree(sw, self.capacity)
        self.southeast = Quadtree(se, self.capacity)

        self.divided = True

    def insert(self, point):
        """
        Add a Point to the Quadtree if it fits within the boundary.
        """
        if not self.boundary.contains(point):
            return False

        if len(self.points) < self.capacity:
            self.points.append(point)
            return True

        if not self.divided:
            self.divide()

        # Attempt to insert into one of the child Quadtrees
        if self.northeast.insert(point): return True
        if self.northwest.insert(point): return True
        if self.southeast.insert(point): return True
        if self.southwest.insert(point): return True

        return False  # Should not reach here

    def query(self, search_range):
        """
        Find all points within a given range (Rectangle).
        """
        found_points = []

        if not self.boundary.intersects(search_range):
            return found_points

        for point in self.points:
            if search_range.contains(point):
                found_points.append(point)

        if self.divided:
            found_points.extend(self.northwest.query(search_range))
            found_points.extend(self.northeast.query(search_range))
            found_points.extend(self.southwest.query(search_range))
            found_points.extend(self.southeast.query(search_range))

        return found_points
