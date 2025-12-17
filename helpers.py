# helpers.py

class Point:
    def __init__(self, x, y, data=None):
        self.x = x
        self.y = y
        self.data = data

class Rectangle:
    def __init__(self, x, y, w, h):
        self.x = x  # Center X
        self.y = y  # Center Y
        self.w = w  # Half-width (distance from center to edge)
        self.h = h  # Half-height (distance from center to edge)

    def contains(self, point):
        return (point.x >= self.x - self.w and
                point.x <= self.x + self.w and
                point.y >= self.y - self.h and
                point.y <= self.y + self.h)

    def intersects(self, range):
        # AABB Collision detection
        return not (range.x - range.w > self.x + self.w or
                    range.x + range.w < self.x - self.w or
                    range.y - range.h > self.y + self.h or
                    range.y + range.h < self.y - self.h)