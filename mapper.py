import matplotlib.pyplot as plt
class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        
    def __repr__(self):
        return f"({self.x}, {self.y})"
    
    def is_equal(self, other):
        if isinstance(other, Point):
            return other.x == self.x and other.y == self.y
        else:
            raise NotImplementedError

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
    
    def get_point_intersecting_perpendicular(self, perpendicular_pont: Point):
        return Point(x=perpendicular_pont.x, y=self.y)
    
    def __repr__(self):
        return f"Horizontal line with y={self.y}, beginning {self.beginning} and ending {self.ending}"
    
class VerticalLine(Line):
    def __init__(self, beginning: Point, ending: Point):
        assert beginning.x == ending.x, "Vertical line must have the same x value"
        super().__init__(beginning=beginning, ending=ending)
        self.x = beginning.x
        
    def is_point_in_line(self, point: Point):
        return point.x == self.x
    
    def get_point_intersecting_perpendicular(self, perpendicular_pont: Point):
        return Point(x=self.x, y=perpendicular_pont.y)
    
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
    
    def get_point_intersecting_perpendicular(self, perpendicular_pont: Point):
        a = self.ending.x
        b = self.ending.y
        c = perpendicular_pont.x
        d = perpendicular_pont.y
        m = self.m
        
        numerator = (-(m**2)*a)+ (m * b) - (m * d) - c
        denominator = -1 - (m**2)
        x = numerator / denominator
        y = (m * x) - (m * a) + b
        
        return Point(x=x, y=y)
    
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
                
    return lines
    
# Points for rectangle example
# points = [Point(x=0, y=0), Point(x=0, y=3), Point(x=0, y=6), Point(x=4, y=6), Point(x=8, y=6), Point(x=8, y=3), Point(x=8, y=0), Point(x=4, y=0), Point(x=0, y=0)]
# Points for triangle example
# points = [Point(x=0, y=0), Point(x=2, y=3), Point(x=4, y=6), Point(x=6.5, y=3), Point(x=9, y=0), Point(x=5, y=0), Point(x=0, y=0)]
# get_lines_in_shape(points=points)

def get_edges_of_shape(points: list[Point]) -> list[Point]:
    """
    Get edges of the shape formed by the points
    """
    lines = get_lines_in_shape(points=points)
    print(f"We have {len(lines)} lines: {lines}")
    edges: list[Point] = []
    
    for index, line in enumerate(lines):
        # If first line take beginning  and ending point
        if index == 0:
            edges.append(line.beginning)
            edges.append(line.ending)
        
        # If middle point get ending
        elif index < len(lines) - 1:
            edges.append(line.ending)
        
        # If last line check if end point same as first line starting point
        else:
            if not edges[0].is_equal(line.ending):
                edges.append(line.ending)
                
    return edges

def plot_shape(points: list[Point]):
    """
    Plot shape from lines in point
    """
    edges = get_edges_of_shape(points=points)
    
    # Plot edges
    x_coords = [e.x for e in edges]
    y_coords = [e.y for e in edges]
    
    # Add first coordinate to end to draw final line
    x_coords.append(x_coords[0])
    y_coords.append(y_coords[0])
    
    print("x coords", x_coords)
    print("y coords", y_coords)
    
    plt.plot(x_coords, y_coords, color='blue', linewidth=2)
    plt.xlabel("X-axis")
    plt.ylabel("Y-axis")
    plt.title("Plotting Shape From Points")
    plt.axis('equal') # Ensures the square is not stretched
    plt.grid(True)
    plt.savefig('shape.png', dpi=300, bbox_inches='tight')
    
    
# edges = get_edges_of_shape(points=points)
# print(f"There are {len(edges)} edges in shape")
# print(edges)
# plot_shape(points=points)

slanted_line = SlantedLine(beginning=Point(x=0, y=0), ending=Point(x=4, y=6))
other_point = Point(x=7, y=4)
print(f"Point intersecting perpendicular line from {other_point} and {slanted_line} is {slanted_line.get_point_intersecting_perpendicular(other_point)}")