# Show the solution path on the existing maze on turtle window
# Process click co-ordinates (for endpoints), extract the cell indices, store them

# from turtle import tracer, update
from DrawMaze import DrawMaze


# Draw maze solution
class ShowPath:

    # Accept solution path, draw_obj for co-ordinates calculation, turtle to draw path with
    def __init__(self, draw_obj, path_turtle, delay_=2):
        self.delay = delay_
        self.unit = draw_obj.unit
        self.width = draw_obj.width
        self.ref = draw_obj.ref
        self.pathTurtle = path_turtle
        self.pathTurtle.color("red")
        self.screen = self.pathTurtle.getscreen()
        self.screen.tracer(1)
        DrawMaze.configTurtle(self.pathTurtle, self.width)

    # Draw the solution path with given turtle
    def draw(self, path):

        t2 = self.pathTurtle

        # turtle configurations
        refRate = (len(path)//20)*3
        self.screen.tracer(refRate, self.delay)
        # DrawMaze.configTurtle(t2)

        # Calculate co-ordinates from cell indices, and draw a dot
        self.markEndPoint(path[0])
        for cell in path[1:]:
            self.unitDraw(cell)
        self.markEndPoint(path[-1])
        self.screen.update()

    def markEndPoint(self, cell):
        center = self.getCellCenter(cell)
        t2 = self.pathTurtle
        t2.up()
        t2.goto(center)
        t2.dot(self.unit/2)

    def unitDraw(self, next_cell):
        center = self.getCellCenter(next_cell)
        t2 = self.pathTurtle
        t2.down()
        t2.goto(center)

    def getCellCenter(self, cell):
        ref, unit = self.ref, self.unit
        loc = (ref[0] + cell[1] * unit,
               ref[1] - cell[0] * unit)
        center = (loc[0] + unit / 2,
                  loc[1] - unit / 2)
        return center

