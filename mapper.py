class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

class Line:
    def __init__(self, beginning: Point, ending: Point):
        self.beginning = beginning
        self.ending = ending
    
    def set_beginning(self, beginning: Point):
        self.beginning = beginning
        
    def set_ending(self, ending: Point):
        self.ending = ending
    
class HorizontalLine(Line):
    def __init__(self, beginning: Point, ending: Point):
        assert beginning.y == ending.y, "Horizontal line must have the same y value"
        self.y = beginning.y
        
    def is_point_part_line(self, point: Point):
        return self.y == point.y
    
class VerticalLine(Line):
    def __init__(self, beginning: Point, ending: Point):
        assert beginning.x == ending.x, "Vertical line must have the same x value"
        self.x = beginning.x
        
    def is_point_in_line(self, point: Point):
        return point.x == self.x
    
class SlantedLine(Line):
    def __init__(self, beginning: Point, ending: Point):
        assert beginning.x != ending.x, "Slanted line can't be vertical"
        assert beginning.y != ending.y, "Slanted line can't be horizontal"
        
        self.m = (ending.y - beginning.y) / (ending.x - beginning.x)
        
    def is_point_in_line(self, point: Point):
        # Check if line is vertical
        is_vertical = self.ending.x == point.x
        
        if is_vertical:
            return False
        
        # Use slope method
        d = point.y
        c = point.x
        a = self.ending.x
        b = self.ending.y
        return d == (self.m * (c-a)) + b
    
    