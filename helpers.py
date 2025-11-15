# helpers.py
# This file holds the "blueprints" for our data.
# Both teams will use these blueprints.

class Point:
    """A simple class to represent a 2D point (x, y)."""
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        # You can add more data here later, like `price` or `bedrooms`
        # self.price = price 

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
        
        # This logic checks if the point's x is between the
        # rectangle's left edge (x) and right edge (x + width),
        # and if the point's y is between the top edge (y)
        # and bottom edge (y + height).
        
        return (self.x <= point.x < self.x + self.width and
                self.y <= point.y < self.y + self.height)
    
    def intersects(self, other_range):
        """Check if another Rectangle object overlaps with this one."""
        
        # This logic is the opposite of "do they NOT overlap?"
        # If any of these are true, they do NOT overlap.
        if (other_range.x + other_range.width < self.x or  # other is to the left
            other_range.x > self.x + self.width or      # other is to the right
            other_range.y + other_range.height < self.y or  # other is above
            other_range.y > self.y + self.height):     # other is below
            return False
            
        # If none of the "no overlap" conditions are met, they must overlap.
        return True