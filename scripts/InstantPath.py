# Show path between any two points within the maze

from scripts.SolveMaze import SolveMaze
from scripts.ShowPath import ShowPath


class InstantPath:

    def __init__(self, path_turtle, draw_obj, maze_obj):
        self.pathTurtle = path_turtle
        self.pathObj = CustomEndPoints(path_turtle, draw_obj, maze_obj.dim)
        self.drawObj = draw_obj
        self.mazeObj = maze_obj
        self.screen = self.pathTurtle.getscreen()
        self.screen.onscreenclick(self.firstClick)

    # Function triggered by first click (actually an odd numbered click)
    def firstClick(self, x, y):
        self.pathTurtle.clear()                          # Clear the previously drawn path
        isValid = self.pathObj.setEndPoint(x, y)         # Check if clicked inside the maze, then record that endpoint
        if isValid:
            self.screen.onscreenclick(self.secondClick)  # If clicked inside the maze, expect the second endpoint

    # Function triggered after first endpoint (start) fetched successfully
    def secondClick(self, x, y):
        isValid = self.pathObj.setEndPoint(x, y)         # Again, click validity check and endpoint record
        if isValid:
            endPoints = self.pathObj.endPoints           # Fetch both endpoint (start and end)
            solveObjTemp = SolveMaze(self.mazeObj,       # Return the solution path for the given endpoints and the maze
                                     *endPoints)
            ShowPath(self.drawObj, self.pathTurtle,         # Call the path drawing routine with required parameters
                     delay_=0).draw(solveObjTemp.path)
            self.screen.onscreenclick(self.firstClick)   # To accept new endpoints pair from user, consider the next
            #                                            # click as the first click, and repeat for new paths


# Process and store custom endpoints
class CustomEndPoints:

    def __init__(self, path_turtle, draw_obj, dim):
        self.endPoints = []                             # Store initial and final cell indices
        self.pathTurtle = path_turtle
        self.ref = draw_obj.ref
        self.unit = draw_obj.unit
        self.dim = dim

        self.SP_obj = ShowPath(draw_obj, path_turtle)

    # Core endpoints method
    def setEndPoint(self, x, y):
        cell = self.fetchCell(x, y)                     # Fetch cell indices for given co-ordinates,
        if cell == -1:                                      # continue further if valid - clicked inside the maze
            return 0
        if len(self.endPoints) == 2:                    # Remove the previous pair of endpoints
            self.endPoints = []
        self.endPoints.append(cell)                     # Add the cell in endpoints list
        self.SP_obj.markEndPoint(cell)
        return 1

    # Find the cell given the click co-ordinates, and validate
    def fetchCell(self, x, y):
        refX, refY = self.ref[0], self.ref[1]
        unit, dim = self.unit, self.dim
        col = (x - refX)//unit                          # Cell column number and row number, as per the co-ordinates
        row = (refY - y)//unit
        if 0 <= row < dim[0] and 0 <= col < dim[1]:     # Validate the calculated indices
            cell = (int(row), int(col))
            return cell
        return -1
