# Random Maze Generation through Recursive Backtracking (Randomised DFS)

import random


class CreateMaze:

    # Possible difference of two adjacent cells
    shift = ((-1, 0), (0, 1), (1, 0), (0, -1))

    # Common wall bit index from the shift (difference) calculated from the adjacent cell
    dirIndex = {(-1, 0): 1, (0, 1): 2, (1, 0): 3, (0, -1): 4}

    # Accept the parameters; initiate maze matrix with default values; initiate maze creation
    def __init__(self, dim, seed=random.seed()):
        self.dim = dim
        self.seed = seed
        random.seed(seed)

        # 7 as prefix: cells are unvisited
        self.maze = [[70000] * dim[1] for _rows in range(dim[0])]
        self.recBacktrack()

    # Random maze generation routine: Recursive Backtracking
    def recBacktrack(self):
        loc = initial = (0, 0)                  # Starting/Current cell
        self.markVisited(loc)                   # Mark the starting cell 'visited': change the prefix to 8
        while 1:
            adj = self.unvisited(loc)           # Find a random unvisited neighbour
            if adj:                             # If there is such neighbour
                self.breakWall(loc, adj)        # Carve path to the neighbour by breaking the common wall
                loc = adj                       # Repeat the process with the neighbour as the current cell
            else:                               # If no unvisited neighbour
                self.markExplored(loc)          # Mark the current cell 'explored': change cell prefix to 9
                if loc == initial:              # Done when reached (back to) the initial cell,
                    break                           # and no neighbour remained unvisited
                loc = self.backTrack(loc)       # Backtrack when no unvisited neighbour

    # Mark the cell as visited, by changing its prefix to 8
    def markVisited(self, loc):
        maze = self.maze
        cell = maze[loc[0]][loc[1]]
        newCell = int('8' + str(cell)[1:])
        maze[loc[0]][loc[1]] = newCell

    # Check if the cell has been visited previously - the prefix must have changed from 7
    def isVisited(self, loc):
        maze = self.maze
        cell = maze[loc[0]][loc[1]]
        status = str(cell)[0]
        ans = False if status == '7' else True
        return ans

    # Find neighbouring cells; find and keep unvisited cells; choose one randomly
    def unvisited(self, loc):
        adj = self.neighbour(loc)
        unseen = []
        for a in adj:
            if not self.isVisited(a):
                unseen.append(a)
        lucky = random.choice(unseen) if unseen else 0
        return lucky

    # Find valid neighbours - inside maze boundary
    def neighbour(self, loc):
        adj = []
        # CreateMaze.shift => ((-1, 0), (0, 1), (1, 0), (0, -1))
        for s in CreateMaze.shift:
            newLoc = (loc[0]+s[0], loc[1]+s[1])             # Adjacent cell indices
            if 0 <= newLoc[0] < self.dim[0] \
                    and 0 <= newLoc[1] < self.dim[1]:       # Check if valid maze cell indices
                adj.append(newLoc)
        return adj

    # Break the common wall between given two cells
    def breakWall(self, loc, adj):

        locShift = (adj[0] - loc[0], adj[1] - loc[1])       # Find the shift (difference) among the two cells
        adjShift = (-locShift[0], -locShift[1])

        # CreateMaze.dirIndex =>
        # {(-1, 0): 1, (0, 1): 2, (1, 0): 3, (0, -1): 4}
        locIndex = CreateMaze.dirIndex[locShift]            # Find the direction of the wall for both the cells
        adjIndex = CreateMaze.dirIndex[adjShift]

        self.toggleWall(loc, locIndex)                      # Toggle the wall (bit) at index given by dirIndex
        self.toggleWall(adj, adjIndex)                      # For the 9-N-E-S-W format, Eastern wall = Index 2

        self.markVisited(adj)                               # Mark the neighbour as visited

    # Toggle the wall of the given cell at the given index
    def toggleWall(self, cell, idx):
        value = self.maze[cell[0]][cell[1]]                 # Get the cell value (number)
        digits = list(str(value))                           # Convert to a list of digits as string tokens
        digits[idx] = '0' if digits[idx] == '1' else '1'    # Flip the wall indicator at the given index
        newValue = int(''.join(digits))                     # Join the characters back to an integer
        self.maze[cell[0]][cell[1]] = newValue              # Update the cell value

    # Backtrack to the previous cell
    def backTrack(self, loc):
        acc = self.accessible(loc)                          # Adjacent cells accessible from the current one
        prev = (None, None)
        if len(acc) == 1:                                   # If only one accessible cell, it's the previous
            prev = acc[0]
        else:
            for a in acc:                                   # Out of many accessible cells,
                if not self.isExplored(a):                      # backtrack to the unexplored one
                    prev = a
                    break
        return prev

    # Check if the current cell is explored - visited and also backtracked
    def isExplored(self, loc):
        cell = self.maze[loc[0]][loc[1]]
        status = str(cell)[0]
        ans = True if status == '9' else False              # Prefix 9 for the explored cells
        return ans

    # Mark the current cell as explored - change the prefix to 9
    def markExplored(self, loc):
        cell = self.maze[loc[0]][loc[1]]
        self.maze[loc[0]][loc[1]] = int('9'+str(cell)[1:])

    # Find the adjacent cells which are accessible (directly) - nearby cell with no wall in between
    def accessible(self, loc):
        adj = self.neighbour(loc)
        acc = []
        for a in adj:
            if not self.wallBetween(loc, a):
                acc.append(a)
        return acc

    # Check (and return) if a wall in between the given two cells
    def wallBetween(self, loc, adj):
        shift = (adj[0] - loc[0], adj[1] - loc[1])

        # dirIndex => {(-1, 0): 1, (0, 1): 2, (1, 0): 3, (0, -1): 4}
        idx = CreateMaze.dirIndex[shift]
        cell = self.maze[loc[0]][loc[1]]
        if str(cell)[idx] == '0':
            return idx
        return 0
