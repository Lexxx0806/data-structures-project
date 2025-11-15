# helpers.py
# This file holds the "blueprints" for our data.

class Point:
    """A simple class to represent a 2D point (x, y)."""
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Rectangle:
    """A class to represent a rectangle.
    
    'x' and 'y' are the top-left corner coordinates.
    """
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def contains(self, point):
        """Check if a Point object is inside this rectangle."""
        return (self.x <= point.x < self.x + self.width and
                self.y <= point.y < self.y + self.height)
    
    def intersects(self, other_range):
        """Check if another Rectangle object overlaps with this one."""
        # Returns True if rectangles do NOT overlap
        if (other_range.x + other_range.width < self.x or
            other_range.x > self.x + self.width or
            other_range.y + other_range.height < self.y or
            other_range.y > self.y + self.height):
            return False
        return True