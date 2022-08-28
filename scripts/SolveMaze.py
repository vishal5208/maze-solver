# Solve the given maze, using DFS, for passed initial and final endpoints,
# or default - initial: top-left cell, final: bottom-right cell

from copy import deepcopy


# Reset the cells' prefixes to a new_prefix, for code reuse
def resetPrefix(maze_obj, new_prefix):
    maze = maze_obj.maze
    dim = maze_obj.dim
    for row in range(dim[0]):
        for col in range(dim[1]):
            cell = maze[row][col]
            newCell = int(str(new_prefix) + str(cell)[1:])
            maze[row][col] = newCell


# Solve the maze, store the solution path
class SolveMaze:

    def __init__(self, maze_obj, initial=None, final=None):
        mazeObj = deepcopy(maze_obj)                    # Make a copy of the original maze
        self.path = []                                  # Initialize solution path
        if initial is None:                             # Set default initial and final endpoints
            initial = (0, 0)
        if final is None:
            final = (maze_obj.dim[0] - 1,
                     maze_obj.dim[1] - 1)
        resetPrefix(mazeObj, 7)                         # To consider all cells to be unvisited, change their prefixes
        self.dfs(mazeObj, initial, final)               # Run DFS from initial, looking for final

    # Depth First Search, reusing methods of CreateMaze class
    def dfs(self, maze_obj, initial, final):
        mazeObj = maze_obj                              # The CreateMaze object with walls' information
        loc = initial
        mazeObj.markVisited(loc)                        # Mark the initial cell as visited,
        self.path.append(loc)                               # and include in the solution path
        while loc != final:
            adj = mazeObj.accessible(loc)               # Find adjacent accessible cells,
            unseen = [a for a in adj                        # which are not visited
                      if not mazeObj.isVisited(a)]
            if unseen:                                  # If there is/are such cell(s),
                loc = unseen[0]                         # choose the first (any) one,
                mazeObj.markVisited(loc)                # mark it as visited,
                self.path.append(loc)                   # and include it in the solution path

            else:                                       # If there is no new nearby cell,
                mazeObj.markExplored(loc)               # mark the cell as explored,
                self.path.pop()                         # not a part of solution path - remove it,
                loc = mazeObj.backTrack(loc)            # and backtrack
