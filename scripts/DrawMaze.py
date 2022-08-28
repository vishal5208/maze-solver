# Visualise the maze with turtle module

# from turtle import tracer, update


class DrawMaze:

    # Accept the maze object and the optional screen refresh rate,
    # initialize some other attributes, begin drawing
    def __init__(self, maze_obj, maze_turtle, ref_rate=None):
        self.refRate = ref_rate
        self.unit = None
        self.width = None
        self.ref = None
        self.dim = maze_obj.dim
        self.draw(maze_obj, maze_turtle)

    # Draw the maze on turtle window
    def draw(self, maze_obj, maze_turtle):

        maze = maze_obj.maze
        dim = maze_obj.dim
        t0 = maze_turtle
        screen = t0.getscreen()

        self.calcUnit(dim, screen)                              # Find appropriate unit size
        unit = self.unit
        screen.screensize(dim[1] * unit + 20,
                          dim[0] * unit + 20)                  # (Canvas) Screen size to fit the maze

        self.width = max(2, unit // 10)                 # Vary wall width along with unit, but at least 2 pixels

        DrawMaze.configTurtle(t0, self.width)  # Set turtle properties - visibility, speed, and width

        if self.refRate is None:                        # Calculate a default refresh rate
            self.refRate = (dim[0]*dim[1])//10*5
        screen.tracer(self.refRate, 0)                  # Set the screen refresh rate for the drawing, and delay to 0
        t0.setheading(270)                                 # Initially turtle heads towards South
        t0.up()                                            # Pen up (No drawing while moving)

        self.ref = (-dim[1] / 2 * unit,                 # Consider top left corner of the first cell
                    dim[0] / 2 * unit)                      # as the reference
        for y in range(dim[0]):                         # Iterate through all the cells
            for x in range(dim[1]):
                start = (self.ref[0] + x * unit,        # Find top left corner of the current cell
                         self.ref[1] - y * unit)            # using the reference and the cell indices
                t0.goto(start)
                cell = maze[y][x]                       # Get the cell (walls) information

                for access in str(cell)[1:][::-1]:      # Read for the presence of each wall in the reverse order
                    if access == '0':                   # If wall present, draw by pulling the pen down
                        t0.down()
                    t0.forward(unit)                       # Forward and left - move along the cell boundary
                    t0.left(90)
                    t0.up()
        screen.update()                                 # Explicitly refresh the screen when completed

    # Vary the unit (cell) size based on window measurements and maze dimensions
    def calcUnit(self, dim, screen):
        wHeight = screen.window_height()
        wWidth = screen.window_width()
        rows = dim[0]
        columns = dim[1]
        unit = min(wHeight / (rows + 1),                # Calculate unit, with which maze would
                   wWidth / (columns + 1))                  # tightly fit the window
        unit = min(50, unit)                            # Bound the unit value from both the sides
        unit = max(10, unit)                                # to avoid undesirable maze size
        unit = (unit // 2) * 2                          # Round the unit to lower even number to avoid jagged lines
        self.unit = unit

    @staticmethod
    # Set some common turtle properties
    def configTurtle(turtle1, width_=None):
        turtle1.hideturtle()
        turtle1.speed(0)
        if width_:
            turtle1.width(width_)
