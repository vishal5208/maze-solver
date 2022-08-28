# Allow user to solve the maze through arrow keys

from scripts.ShowPath import ShowPath


class PlayerMode:
    
    def __init__(self, maze_obj, draw_obj, path_turtle):
        self.mazeObj = maze_obj
        self.drawObj = draw_obj
        self.pathTurtle = path_turtle
        self.screen = path_turtle.getscreen()
        self.SP_obj = ShowPath(draw_obj, path_turtle)

        self.loc = self.initial = (0, 0)
        self.final = (maze_obj.dim[0] - 1, maze_obj.dim[1] - 1)
        # self.final = (0, 1)
        self.path = [self.initial]

        self.pathTurtle.clear()
        self.SP_obj.markEndPoint(self.final)
        self.SP_obj.markEndPoint(self.initial)

        self.screen.listen()
        self.handleKeyEvents("ON")

    def handleKeyEvents(self, switch):
        
        screen = self.screen

        if switch == "ON":
            screen.onkey(lambda: self.move('Up'), 'Up')
            screen.onkey(lambda: self.move('Down'), 'Down')
            screen.onkey(lambda: self.move('Left'), 'Left')
            screen.onkey(lambda: self.move('Right'), 'Right')

        elif switch == "OFF":
            screen.onkey(lambda: None, 'Up')
            screen.onkey(lambda: None, 'Down')
            screen.onkey(lambda: None, 'Left')
            screen.onkey(lambda: None, 'Right')

    def move(self, direction):
        adj = self.nextCell(direction)
        if adj:
            self.loc = adj
            if len(self.path) >= 2 and adj == self.path[-2]:
                self.path.pop()
                self.pathTurtle.undo()
            else:
                self.path.append(adj)
                self.SP_obj.unitDraw(adj)
                if self.loc == self.final:
                    self.congratulate()
                    self.handleKeyEvents("OFF")

    def nextCell(self, direction):
        shift = {'Up': (-1, 0), 'Right': (0, 1),
                 'Down': (1, 0), 'Left': (0, -1)}
        delta = shift[direction]
        adj = (self.loc[0] + delta[0], self.loc[1] + delta[1])
        acc = self.mazeObj.accessible(self.loc)
        if adj in acc:
            return adj
        return 0

    def congratulate(self):
        t2 = self.pathTurtle
        ref, unit, dim = self.drawObj.ref, self.drawObj.unit, self.drawObj.dim
        coord = (ref[0] + unit * dim[1]/2,
                 ref[1] - unit * dim[0] - 30)
        t2.up()
        t2.goto(coord)
        t2.write("CONGRATULATIONS", False,
                 "center", ("Verdana", 15, "bold"))
