# Run the command in terminal : python3 scripts/CoreGUI.py

# Project details 

 ## Abstract 

The project can generate random perfect mazes of given dimensions, store them as matrices, and show them pictorially. It can solve for typical endpoints - start being the top left cell and stop being the bottom right cell - or solve for any selected endpoints in the maze which the user feeds during runtime by clicking within the maze. It can also allow the user to solve it by navigating through the maze with arrow keys. The algorithm used to generate the random maze is Recursive Backtracker also known as Randomised Depth First Search and the one to solve it is Depth First Search (DFS).

## Maze Generation ##
The algorithm implemented for generating random perfect mazes is the Recursive Backtracker also known as Randomized Depth First Search. The algorithm is fed with the required dimensions of the maze with an optional seed for the random sequence, and the output is the matrix representation of the corresponding random perfect maze. It initially starts with a matrix of the given dimensions where each element is 70000, which means the cells are unvisited and none of the neighbours are accessible (all walls present - as a grid). It begins with the top-left cell, marks it as visited by changing its prefix to 8, and randomly visits a neighbour - marks it as visited and removes the common wall by changing the corresponding bit in both the cells. It continues from that neighbouring cell as the current cell, looks for an unvisited neighbour, if more than one such neighbour is available, it chooses one randomly. If no such unvisited neighbour is found, the cell is marked explored by changing the prefix to 9 and tries to backtrack to the previous cell. The previous cell is not stored, but determined by finding the cells accessible from the current cell, and selecting the cell out of them which isn’t marked explored yet (only one such exists). The process continues until it backtracks to the initial cell and it doesn’t have any unvisited neighboring cells, which implies that every cell has been traversed and the perfect maze is ready.

## Maze Solution 
The algorithm implemented to solve the given maze is the Depth First Search algorithm. This graph algorithm is used by considering the maze as a graph where each cell is a node and two nodes have an edge between them if the two corresponding cells do not have the common wall, i.e., they are accessible from each other. The algorithm accepts the maze in a matrix form, and the start and stop (initial and final cells), each one as a pair of corresponding indices in the matrix, e.g. (0, 0) would mean the top-left cell (typical starting point). The output is the sequence of the cells (list of pairs of indices), following which would lead to the solution of the maze. It begins with the initial cell, marks it as visited and adds to the solution sequence. Then looks for unvisited accessible neighbors and picks one (almost randomly), moves to that cell, marks it as visited and adds to the solution sequence, and repeats. If it comes across a deadend - a cell with no accessible neighbor which is unvisited - it marks the current cell as explored and removes it from the solution sequence. Then, it backtracks by finding the unexplored accessible neighboring cell and resumes from there. It halts when it comes across the final cell, which always happens in our case as the input maze is a perfect maze, and hence always has one unique path.