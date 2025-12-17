# This is for quadtree.py
from helpers import Rectangle

class Quadtree:
    def __init__(self, boundary, capacity):
        self.boundary = boundary
        self.capacity = capacity
        self.points = []
        self.divided = False

    def subdivide(self):
        x, y, w, h = self.boundary.x, self.boundary.y, self.boundary.w / 2, self.boundary.h / 2
        self.ne = Quadtree(Rectangle(x + w, y - h, w, h), self.capacity)
        self.nw = Quadtree(Rectangle(x - w, y - h, w, h), self.capacity)
        self.se = Quadtree(Rectangle(x + w, y + h, w, h), self.capacity)
        self.sw = Quadtree(Rectangle(x - w, y + h, w, h), self.capacity)
        self.divided = True

    def insert(self, point):
        if not self.boundary.contains(point): return False
        if len(self.points) < self.capacity:
            self.points.append(point)
            return True
        if not self.divided: self.subdivide()
        return (self.ne.insert(point) or self.nw.insert(point) or self.se.insert(point) or self.sw.insert(point))

    def query(self, range, found):
        if not self.boundary.intersects(range): return
        for p in self.points:
            if range.contains(p): found.append(p)
        if self.divided:
            self.ne.query(range, found); self.nw.query(range, found)
            self.se.query(range, found); self.sw.query(range, found)
        return found