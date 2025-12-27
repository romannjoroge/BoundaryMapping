class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        
    def __repr__(self):
        return f"({self.x}, {self.y})"

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
        super().__init__(beginning=beginning, ending=ending)
        self.y = beginning.y
        
    def is_point_part_line(self, point: Point):
        return self.y == point.y
    
    def __repr__(self):
        return f"Horizontal line with y={self.y}, beginning {self.beginning} and ending {self.ending}"
    
class VerticalLine(Line):
    def __init__(self, beginning: Point, ending: Point):
        assert beginning.x == ending.x, "Vertical line must have the same x value"
        super().__init__(beginning=beginning, ending=ending)
        self.x = beginning.x
        
    def is_point_in_line(self, point: Point):
        return point.x == self.x
    
    def __repr__(self):
        return f"Vertical line with x={self.x}, beginning {self.beginning} and ending {self.ending}"
    
class SlantedLine(Line):
    def __init__(self, beginning: Point, ending: Point):
        assert beginning.x != ending.x, "Slanted line can't be vertical"
        assert beginning.y != ending.y, "Slanted line can't be horizontal"
        
        super().__init__(beginning=beginning, ending=ending)
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
    
    def __repr__(self):
        return f"Slanted line with slope={self.m}, beginning {self.beginning} with ending {self.ending}"
    
def create_line(beginning: Point, ending: Point) -> Line:
    """
    A function that returns the line that joins the beginning and end point
    
    The returned line can either be vertical, horizontal or slanted
    """
    # Check if line is vertical
    if beginning.x == ending.x:
        return VerticalLine(beginning=beginning, ending=ending)
    
    # Check if line is horizontal
    elif beginning.y == ending.y:
        return HorizontalLine(beginning=beginning, ending=ending)
    
    # Return slanted line
    else:
        return SlantedLine(beginning=beginning, ending=ending)
    
def check_if_point_in_line(line: Line, point: Point) -> bool:
    if isinstance(line, HorizontalLine):
        return line.is_point_part_line(point=point)
    elif isinstance(line, VerticalLine):
        return line.is_point_in_line(point=point)
    elif isinstance(line, SlantedLine):
        return line.is_point_in_line(point=point)
    else:
        raise NotImplementedError
    
def get_lines_in_shape(points: list[Point]) -> list[Line]:
    """
    Takes points and from those points gets the lines in shape
    """
    lines = []
    beginning_point: Point = None
    ending_point: Point = None
    
    for point in points:
        print(f"Processing point {point}")
        if len(lines) == 0:
            if beginning_point == None:
                beginning_point = point
            elif ending_point == None:
                ending_point = point
                first_line = create_line(beginning=beginning_point, ending=point)
                lines.append(first_line)
            else:
                raise "A line should be there"
        else:
            line_to_check: Line = lines[-1]
            if check_if_point_in_line(line=line_to_check, point=point):
                line_to_check.set_ending(point)
            else:
                new_line = create_line(beginning=line_to_check.ending, ending=point)
                lines.append(new_line)
                
    print(f"We have {len(lines)} lines")
    print(lines)
            
points = [Point(x=0, y=0), Point(x=0, y=3), Point(x=0, y=6), Point(x=4, y=6), Point(x=8, y=6), Point(x=8, y=3), Point(x=8, y=0), Point(x=4, y=0), Point(x=0, y=0)]
get_lines_in_shape(points=points)