# Core maze program - calling all the maze components

from scripts.CreateMaze import CreateMaze
from DrawMaze import DrawMaze
from scripts.SolveMaze import SolveMaze
from scripts.ShowPath import ShowPath
from scripts.InstantPath import InstantPath
from scripts.UserSolvesMaze import PlayerMode

from turtle import RawTurtle, TurtleScreen

from tkinter import *
from tkinter import ttk


class MazeGUI:

    def __init__(self):

        self.root = Tk()
        self.root.title("Maze Solver")

        # Maze Canvas
        frame1 = ttk.Frame(self.root)
        frame1.grid(column=0, row=0)
        canvas = Canvas(frame1, width=800, height=700)
        canvas.grid(column=0, row=0, padx=10, pady=10)
        self.screen = TurtleScreen(canvas)

        self.mazeTurtle = RawTurtle(self.screen)
        self.pathTurtle = RawTurtle(self.screen)
        self.pathTurtle.hideturtle()

        self.rows = StringVar()
        self.columns = StringVar()
        self.seed = StringVar()

        self.mazeObj = self.drawObj = self.playerObj = None

        self.instantRB = self.userSolveRB = None

        self.createWidgets()
        self.setupWindow()
        self.generateFunc()

    def createWidgets(self):

        ttk.Style().configure('heading.TLabel', font=('theDefaultONE', 10, 'bold'))

        frame2 = ttk.Frame(self.root)
        frame2.grid(column=1, row=0)
        ttk.Label(frame2, text="Random Maze Generation", style='heading.TLabel') \
            .grid(column=0, row=0, columnspan=3, sticky='w', padx=2, pady=20)

        ttk.Label(frame2, text="No. of Rows:"). \
            grid(column=0, row=1, sticky='w', padx=2, pady=2)
        self.rows.set(7)
        ttk.Entry(frame2, width=7, textvariable=self.rows) \
            .grid(column=1, row=1, padx=2, pady=2)

        ttk.Label(frame2, text="No. of Columns:") \
            .grid(column=0, row=2, sticky='w', padx=2, pady=2)
        self.columns.set(10)
        ttk.Entry(frame2, width=7, textvariable=self.columns) \
            .grid(column=1, row=2, padx=2, pady=2)

        ttk.Label(frame2, text="Seed (Optional):") \
            .grid(column=0, row=3, sticky='w', padx=2, pady=2)
        ttk.Entry(frame2, width=7, textvariable=self.seed) \
            .grid(column=1, row=3, padx=2, pady=2)

        generateB = ttk.Button(frame2, text=" Generate \n the maze ", command=self.generateFunc)
        generateB.grid(column=2, row=1, rowspan=3, sticky="n s w", padx=(8, 12), pady=2)

        ttk.Label(frame2, text=" ").grid(column=0, row=4)
        ttk.Label(frame2, text="Maze Solution", style='heading.TLabel') \
            .grid(column=0, row=5, columnspan=2, sticky='w', padx=2, pady=20)

        solveB = ttk.Button(frame2, text="Solve", command=self.solveFunc)
        solveB.grid(column=2, row=5, sticky="w", padx=8, pady=2)

        ttk.Label(frame2, text="Interactive Functions", style='heading.TLabel') \
            .grid(column=0, row=6, columnspan=3, sticky='w', padx=2, pady=20)

        self.instantRB = ttk.Radiobutton(frame2, text="Instant Path", value=1, command=self.instantFunc)
        self.instantRB.grid(column=0, row=7, columnspan=3, sticky='w', padx=2, pady=2)

        self.userSolveRB = ttk.Radiobutton(frame2, text="User Attempt", value=2, command=self.userSolveFunc)
        self.userSolveRB.grid(column=0, row=8, columnspan=3, sticky='w', padx=2, pady=2)

    def generateFunc(self):

        check = self.checkValues()
        if check == "Invalid":
            return

        r, c, s = check
        if s == "Random Seed":
            mazeObj = CreateMaze((r, c))
        else:
            mazeObj = CreateMaze((r, c), s)

        self.disableInteractive()
        self.pathTurtle.clear()
        self.mazeTurtle.clear()
        drawObj = DrawMaze(mazeObj, self.mazeTurtle, ref_rate=0)

        self.mazeObj = mazeObj
        self.drawObj = drawObj

    def checkValues(self):
        try:
            r, c = int(self.rows.get()), int(self.columns.get())
            if r < 1 or c < 1:
                return "Invalid"
            try:
                s = int(self.seed.get())
                if s < 0:
                    raise ValueError
                return r, c, s
            except ValueError:
                self.seed.set('')
                return r, c, "Random Seed"
        except ValueError:
            return "Invalid"

    def solveFunc(self):
        self.disableInteractive()
        mazeObj, drawObj = self.mazeObj, self.drawObj
        solveObj = SolveMaze(mazeObj, initial=(0, 0))
        self.pathTurtle.clear()
        ShowPath(drawObj, self.pathTurtle,
                 delay_=10).draw(solveObj.path)

    def disableInteractive(self):
        self.disableInstant()
        self.disableUserSolve()

    def disableInstant(self):
        self.instantRB.state(["!focus", "!selected"])
        self.screen.onscreenclick(lambda x, y: None)

    def disableUserSolve(self):
        self.userSolveRB.state(["!focus", "!selected"])
        if self.playerObj:
            self.playerObj.handleKeyEvents("OFF")

    def instantFunc(self):
        self.disableUserSolve()
        mazeObj, drawObj = self.mazeObj, self.drawObj
        InstantPath(self.pathTurtle, drawObj, mazeObj)

    def userSolveFunc(self):
        self.disableInstant()
        mazeObj, drawObj = self.mazeObj, self.drawObj
        playerObj = PlayerMode(mazeObj, drawObj, self.pathTurtle)
        self.playerObj = playerObj

    def setupWindow(self):
        root = self.root
        root.update()
        w = root.winfo_width()
        h = root.winfo_height()
        ws = root.winfo_screenwidth()
        hs = root.winfo_screenheight()
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2) - 15
        self.root.geometry('%dx%d+%d+%d' % (w, h, x, y))


mazeSolver = MazeGUI()
mazeSolver.root.mainloop()
