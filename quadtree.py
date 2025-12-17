
# quadtree.py
from helpers import Rectangle, Point
from typing import List, Optional

class Quadtree:
    def __init__(self, boundary: Rectangle, capacity: int):
        self.boundary = boundary
        self.capacity = capacity
        self.points: List[Point] = []
        self.divided: bool = False
        # Initialize children as None to save memory
        self.ne: Optional[Quadtree] = None
        self.nw: Optional[Quadtree] = None
        self.se: Optional[Quadtree] = None
        self.sw: Optional[Quadtree] = None

    def subdivide(self):
        # Create 4 children. 
        # Since x,y are center points, we shift by w (half-width) and h (half-height)
        x, y = self.boundary.x, self.boundary.y
        w, h = self.boundary.w / 2, self.boundary.h / 2
        
        # Northeast (Right, Up) - Remember Y goes down in canvas, so Up is minus
        self.ne = Quadtree(Rectangle(x + w, y - h, w, h), self.capacity)
        # Northwest (Left, Up)
        self.nw = Quadtree(Rectangle(x - w, y - h, w, h), self.capacity)
        # Southeast (Right, Down)
        self.se = Quadtree(Rectangle(x + w, y + h, w, h), self.capacity)
        # Southwest (Left, Down)
        self.sw = Quadtree(Rectangle(x - w, y + h, w, h), self.capacity)
        
        self.divided = True

    def insert(self, point: Point) -> bool:
        if not self.boundary.contains(point):
            return False

        # If there is space and we haven't divided yet, add here
        if len(self.points) < self.capacity and not self.divided:
            self.points.append(point)
            return True

        # If full, split!
        if not self.divided:
            self.subdivide()
            
        # Optimization: Attempt to push point to children
        if self.ne.insert(point): return True
        if self.nw.insert(point): return True
        if self.se.insert(point): return True
        if self.sw.insert(point): return True
        
        return False

    def query(self, range_rect: Rectangle, found: List[Point]) -> List[Point]:
        # Spatial Pruning: If boundaries don't match, stop looking (Big O Optimization)
        if not self.boundary.intersects(range_rect):
            return found

        # Check points at this level
        for p in self.points:
            if range_rect.contains(p):
                found.append(p)

        # Recurse if divided
        if self.divided:
            self.nw.query(range_rect, found)
            self.ne.query(range_rect, found)
            self.sw.query(range_rect, found)
            self.se.query(range_rect, found)
            
        return found
    
    def __len__(self):
        # Helper to count total nodes (useful for debugging)
        count = len(self.points)
        if self.divided:
            count += len(self.nw) + len(self.ne) + len(self.sw) + len(self.se)
        return count
