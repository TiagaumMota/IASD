from tkinter import YView
import search
""" For this assignment, you just need to import search.py,  
which in turn imports utils.py; both files are available 
in the repository mentioned on page 2 of the Assignment"""

class action():
    def __init__ (self, row, col, dir):
        self.row = row
        self.col = col
        self.dir = dir

    def __str__ (self):
        return 'Action: move cell in (' + str(self.row) + ',' + str(self.col) + ') in \'' + str(self.dir) + '\' direction'

class RTBProblem(search.Problem):
    def __init__ (self):
        """Method that instantiate your class.
        You can change the content of this.
        self.initial is where the initial state of the puzzle should be saved. 
        self.algorithm is where the chosen uninformed search algorithm should be saved."""

        self.initial = None
        self.algorithm = None

        self.size = None
        self.xy_initial = None 
        self.xy_goal = None
        
    def getActionCoordinates(self, action):
        if(action.dir == 'l'):
            return (action.row, action.col-1)
        
        if(action.dir == 'r'):
            return (action.row, action.col+1)

        if(action.dir == 't'):
            return (action.row-1, action.col)

        if(action.dir == 'd'):
            return (action.row+1, action.col)
        
        return None

    def result (self, state, action):
        """Return the state that results from executing the given act.
        Action is assumed to be a valid action in the state """
        
        #print("\nSTATE:")
        #print(state)


        #print("ACTION:")
        #print(action)

        #print("CELL MOVING:", state[action.row][action.col])

        new_state = list(list(i) for i in state)
        row, col = self.getActionCoordinates(action)
        #print("action origin cell = ", state[action.row][action.col])

        #print("row =", row, "col = ", col)
        
        new_state[row][col], new_state[action.row][action.col] = new_state[action.row][action.col], new_state[row][col]

        return tuple(tuple(i) for i in new_state)

    def isMovableTile(self, state, row, col):
        if "empty" in state[row][col]:
            return False
        
        if "not" in state[row][col]:
            return False

        if "goal" in state[row][col]:
            return False
        
        if "initial" in state[row][col]:
            return False
        
        return True
     
    def actions(self, state):
        """Return the actions that can be executed in the given state"""
        actions = []

        #print("NEW STATE GETTING ACTIONS")
        # Go through all tiles of the state and search for "empty" ones
        for i in range(self.size):
            for j in range(self.size):
                
                #print("i=", i, "j=", j, "state=", state[i][j])
                # We only want to move "Empty" tiles
                if "empty" not in state[i][j]:
                    #print("continuing...\n")
                    continue

                # left
                if(j-1 >= 0 and self.isMovableTile(state, i, j-1) == True):
                    #print("adding action left ->", state[i][j])
                    actions.append(action(i, j, 'l'))

                # right
                if(j+1 < self.size and self.isMovableTile(state, i, j+1) == True):
                    #print("adding action right ->", state[i][j])
                    actions.append(action(i, j, 'r'))

                # top
                if(i-1 >= 0 and self.isMovableTile(state, i-1, j) == True):
                    #print("adding action top ->", state[i][j])
                    actions.append(action(i, j, 't'))

                # down
                if(i+1 < self.size and self.isMovableTile(state, i+1, j) == True):
                    #print("adding action down ->", state[i][j])
                    actions.append(action(i, j, 'd'))

        #print("\nSTATE=")
        #print(state)
        return actions
    
    def goal_test(self, state):
        
        # Saving initial tile's coordinates
        x_init = self.xy_init[0]
        y_init = self.xy_init[1]
        
        direction = None
        origin    = None
        tile      = None

        # Catching the string of the starting tile
        tile_init = state[x_init][y_init]


        # Gathering the direction of the starting tile
        direction = self.getNextDirection(tile_init, "")

        # Also saving where the starting tile is positioned in relation to the tile it is pointing at
        origin = self.getNextOrigin(direction)

        # Initial row and collumn are the ones of the starting tile
        row = x_init
        col = y_init

        while (True):

            # Computing the next tile's coordinates
            (row, col) = self.getNextCoords(row, col, direction)

            # Checking if next tile is within boundaries
            if (not(row >= 0 and row < self.size and col >= 0 and col < self.size)):
                return False

            # Gathering next tile's string
            tile = self.getTileString(state, row, col)

            # Checking if origin is in this new tile
            if origin not in tile:
                return 0
            # Checking if this new tile is the goal
            elif "goal" in tile:
                return True
            else:
                # Compute direction for the next tile
                direction = self.getNextDirection(tile, origin)

                # Save the origin tile to know where we were
                origin = self.getNextOrigin(direction)

    
    def load(self, fh):

        # Loading the whole file
        contents = fh.readlines()

        # Ignoring comment lines
        contentsWithoutComments = [x for x in contents if x[0] != '#']

        # Saving the puzzle's dimensions
        self.size = int(contentsWithoutComments[0])

        # Ignoring string with the dimension
        puzzle = contentsWithoutComments[1:]

        # Turn the puzzle into a matrix
        puzzle = [x.split(' ') for x in puzzle]

        # Searching and saving the starting tile's coordinates
        count_initial = 0
        count_goal = 0
        for i in range(self.size):
            for j in range(self.size):
                if ("initial" in puzzle[i][j]):
                    self.xy_init = [i, j]
                    count_initial += 1
                elif ("goal" in puzzle[i][j]):
                    self.xy_goal = [i, j]
                    count_goal += 1
        
        # Checking if the puzzle has a single starting and ending tile
        if (count_initial != 1 and count_goal != 1):
            return None

        self.initial = tuple(tuple(i) for i in puzzle)
    
    def setAlgorithm(self):
        """Sets the uninformed search algorithm chosen."""
        
        self.algorithm = search.breadth_first_graph_search
        #self.algorithm = search.breadth_first_tree_search
        
        # example: self.algorithm = search.breadth_first_tree search 
        # substitute by the function in search.py that implements the chosen algorithm.
        # You can only use the algorithms defined in search.py

    
    def solve(self):
        """Calls the uninformed search algorithm chosen."""

        return self.algorithm(self)
        #
        # You have to provide the arguments for the chosen algorithm if any.
        # For instance, for the Depth Limited Search you need to provide a value for the limit L, otherwise the default value (50) will be used.

    # Searches for the keyword indicating the direction the current tile faces
    # Receives origin tile so it doesn't go back on the path to the goal
    def getNextDirection(self, tile: str, origin: str):
        if origin != "right" and "right" in tile:
            return "right"
        if origin != "left" and "left" in tile:
            return "left"
        if origin != "top" and "top" in tile:
            return "top"
        if origin != "down" and "down" in tile:
            return "down"

    # Returns the keyword indicating where the previous tile came from
    def getNextOrigin(self, next_direction: str):
        if next_direction == "right":
            return "left"
        if next_direction == "left":
            return "right"
        if next_direction == "top":
            return "down"
        if next_direction == "down":
            return "top"

    # Computes the coordinates of the next tile, according to the direction keyword
    def getNextCoords(self, row: int, col: int, next_direction: str):
        if next_direction == "right":
            return (row, col + 1)
        if next_direction == "left":
            return (row, col - 1)
        if next_direction == "top":
            return (row - 1, col)
        if next_direction == "down":
            return (row + 1, col)
    
    # Returns the keywords for the current tile
    def getTileString(self, state, x: int, y: int):
        return state[x][y]  


fh = open("../tests/pub10.dat", 'r')
rtb = RTBProblem()
rtb.load(fh)
rtb.setAlgorithm()
print(rtb.solve())