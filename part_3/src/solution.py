import search

class action:
    def __init__ (self, row, col, dir):
        """
        Description:\n
            Method that instantiates an action class. Has information 
            about moving a cell in (row, col) in dir direction.\n
            
            self.row: int - row position of the cell
            self.col: int - column position of the cell
            self.dir: int - direction we're moving the cell to
        """
        
        self.row = row
        self.col = col
        self.dir = dir


class RTBProblem(search.Problem):

    def __init__ (self):
        """
        Description:\n
        Method that instantiates an RTBProblem class.\n

        \t self.initial - a dictionary of lists of sets representing the initial state of the puzzle.\n
        \t self.algorithm - the uninformed search algorithm to use.\n
        \t self.size - the number or rows and columns the puzzle has.\n
        \t self.init - the coordinates of the initial/starting cell.\n
        \t self.origins - a dictionary with the opposite direction of every direction.\n
        \t self.nextcoords - a dictionary of functions that compute the coordinates of 
           a cell given  direction and previous coordinates.\n
        """

        self.initial = None
        self.algorithm = None
        self.size = None
        self.init = None

        self.origins = {'r': 'l',
                        'l': 'r',
                        't': 'd',
                        'd': 't'}
        
        self.nextcoords = {'r' : lambda row, col: (row, col+1),
                           'l' : lambda row, col: (row, col-1),
                           't' : lambda row, col: (row-1, col),
                           'd' : lambda row, col: (row+1, col)}


    def result (self, state, action):
        """
        Description:\n
            Computes the state obtained by moving one cell of the puzzle, using information provided in an action object.

        Parameters:\n
            state: dict of lists of sets - representation of a given state, where each set is a cell of the puzzle
            action: action object - information about the action to be executed

        Return:\n
            new_state: dict of lists of sets - the state that results from executing the given action.
        """
        
        # Deepcopying the current state
        new_state = list(list(i) for i in state)

        # Compute the coordinates the empty cell is moving to
        row, col = self.nextcoords[action.dir](action.row, action.col)
        
        # Switching cells
        new_state[row][col], new_state[action.row][action.col] = new_state[action.row][action.col], new_state[row][col]

        new_state = tuple(tuple(i) for i in new_state)
        return new_state

    
    def load(self, fh):
        """
        Description:\n
            Loads a Roll The Boll puzzle from a file and initializes most of the class's attributes.

        Arguments:\n
            fh: file - a file object from which we can read data from the input file

        Return:\n
            None
        """

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
        for row in range(self.size):
            for col in range(self.size):
                
                cell_specs = set()

                # Collect all information about each cell and store it in a set
                if ("initial" in puzzle[row][col]):
                    self.init = (row, col)
                    cell_specs.add('i')
                elif ("goal" in puzzle[row][col]):
                    self.goal = (row, col)
                    cell_specs.add('g')
                elif ("not" in puzzle[row][col]):
                    cell_specs.add('n')
                elif ("empty" in puzzle[row][col]):
                    cell_specs.add('e')
                else:
                    cell_specs.add('m')
                
                if ("left" in puzzle[row][col]):
                    cell_specs.add('l')
                if ("right" in puzzle[row][col]):
                    cell_specs.add('r')
                if ("top" in puzzle[row][col]):
                    cell_specs.add('t')
                if ("down" in puzzle[row][col]):
                    cell_specs.add('d')
                
                puzzle[row][col] = frozenset(cell_specs)
        
        self.initial = tuple(tuple(i) for i in puzzle)

        """
        state = self.initial
        cost = 0

        for row in range(self.size):
            for col in range(self.size):
                
                if ('m' not in state[row][col] or len(state[row][col]) <= 1): continue

                if(row+1 < self.size and self.origins['d'] in state[row+1][col]): continue
                if(row-1 >= 0        and self.origins['t'] in state[row-1][col]): continue
                if(col+1 < self.size and self.origins['r'] in state[row][col+1]): continue
                if(col-1 >= 0        and self.origins['l'] in state[row][col-1]): continue

                print(state[row][col])
                print("(",row,",",col,") is an alone\n")
                cost += 1
        
        print("\ntotal cost = ",cost)
        """
        
        """
        state = self.initial 

        visited = set()

        direction = None
        origin    = None
        tile      = None

        # Initial row and collumn are the ones of the starting tile
        row = self.init[0]
        col = self.init[1]

        visited.add((row,col))

        # Catching the string of the starting tile
        tile_init = state[row][col]

        # Gathering the direction of the starting tile
        direction = self.getNextDirection(tile_init, "")

        # Also saving where the starting tile is positioned in relation to the tile it is pointing at
        origin = self.origins[direction]

        while (True):

            # Computing the next tile's coordinates
            prev_row, prev_col = row,col
            (row, col) = self.nextcoords[direction](row, col)

            # Checking if the next tile is within boundaries
            if (not(row >= 0 and row < self.size and col >= 0 and col < self.size)):
                return self.closest(state, (prev_row, prev_col), visited)

            # Gathering next tile's set (with cell info)
            visited.add((row,col))
            tile = state[row][col]

            # Checking if new tile is connected to the previous one
            if origin not in tile:
                return self.closest(state, (prev_row,prev_col), visited)
            else:
                # Compute direction for the next tile
                direction = self.getNextDirection(tile, origin)

                # Save the origin tile to know where we were
                origin = self.origins[direction]

        """


    def goal_test(self, state):
        """
        Description:\n
            For a given state, checks if there is a path between the initial and the goal cells, meaning the state is a solution.

        Arguments:\n
            state: dict of lists of sets - representation of a given state, where each set is a cell of the puzzle

        Return:\n
            True - if the given state is the solution
            False - otherwise
        """
        
        direction = None
        origin    = None
        tile      = None

        # Initial row and collumn are the ones of the starting tile
        row = self.init[0]
        col = self.init[1]

        # Catching the string of the starting tile
        tile_init = state[row][col]

        # Gathering the direction of the starting tile
        direction = self.getNextDirection(tile_init, "")

        # Also saving where the starting tile is positioned in relation to the tile it is pointing at
        origin = self.origins[direction]

        while (True):

            # Computing the next tile's coordinates
            (row, col) = self.nextcoords[direction](row, col)

            # Checking if the next tile is within boundaries
            if (not(row >= 0 and row < self.size and col >= 0 and col < self.size)):
                return False

            # Gathering next tile's set (with cell info)
            tile = state[row][col]

            # Checking if new tile is connected to the previous one
            if origin not in tile:
                return False

            # Checking if this new tile is the goal cell
            elif 'g' in tile:
                return True
            else:
                # Compute direction for the next tile
                direction = self.getNextDirection(tile, origin)

                # Save the origin tile to know where we were
                origin = self.origins[direction]

     
    def actions(self, state):
        """
        Description:\n
            For a given state, searches the puzzle for empty cells and checks if they can switch position with
            any movable cell, adding it to a list of possible actions.

        Arguments:\n
            state: dict of lists of sets - representation of a given state, where each set is a cell of the puzzle

        Return:\n
            actions: list - a list containing all possible actions, i.e., empty cells switching with a movable cell
        """
        actions = []

        # Go through all tiles of the state and search for "empty" ones
        for row in range(self.size):
            for col in range(self.size):
                
                # We only want to move "empty" tiles
                if "e" not in state[row][col]:
                    continue
                
                # Check if the surrounding cells are movable

                # left
                if(col-1 >= 0 and 'm' in state[row][col-1]):
                    actions.append(action(row, col, 'l'))

                # right
                if(col+1 < self.size and 'm' in state[row][col+1]):
                    actions.append(action(row, col, 'r'))

                # top
                if(row-1 >= 0 and 'm' in state[row-1][col]):
                    actions.append(action(row, col, 't'))

                # down
                if(row+1 < self.size and 'm' in state[row+1][col]):
                    actions.append(action(row, col, 'd'))

        return actions


    def getNextDirection(self, tile: str, origin: str):
        """
        Description:\n
            Given a cell and an the direction of the previous cell (origin), it determines the next direction.

        Arguments:\n
            tile: str - a string which has the directions of the cell
            origin: str - a string of the origin direction

        Return:\n
            str - a string of the next direction 
        """

        if origin != 'r' and 'r' in tile : return 'r'
        if origin != 'l' and 'l' in tile : return 'l'
        if origin != 't' and 't' in tile : return 't'
        if origin != 'd' and 'd' in tile : return 'd'
        #print(tile, origin)

    def h(self, node):
        """ This heuristic works like this:
        . . .
        It is consistent/not consistent because...
        It is admissible/not admissible because..."""
        
        init_cost = self.add_to_visited(node.state, self.init)
        goal_cost = self.add_to_visited(node.state, self.goal)

        return init_cost + goal_cost

    def add_to_visited(self, state, tile):

        visited = set()

        # Initial row and collumn are the ones of the starting tile
        row = tile[0]
        col = tile[1]

        visited.add((row,col))

        # Catching the string of the starting tile
        tile_init = state[row][col]

        # Gathering the direction of the starting tile
        direction = self.getNextDirection(tile_init, "")
        #print(direction)
        # Also saving where the starting tile is positioned in relation to the tile it is pointing at
        origin = self.origins[direction]

        while (True):

            # Computing the next tile's coordinates
            prev_row, prev_col = row,col
            (row, col) = self.nextcoords[direction](row, col)

            # Checking if the next tile is within boundaries
            if (not(row >= 0 and row < self.size and col >= 0 and col < self.size)):
                return self.closest(state, (prev_row, prev_col), visited, origin)

            # Gathering next tile's set (with cell info)
            visited.add((row,col))
            tile = state[row][col]

            # Checking if new tile is connected to the previous one
            if origin not in tile:
                return self.closest(state, (prev_row,prev_col), visited, origin)
            elif "g" in tile or "i" in tile:
                return 0
            else:
                #Add new tile coordinates to set

                # Compute direction for the next tile
                direction = self.getNextDirection(tile, origin)

                # Save the origin tile to know where we were
                origin = self.origins[direction]


    def closest(self, state, tile, visited, origin):

        #visited.add(tile)
        queue = [tile]
        cost = 1

        while queue:
            
            x,y = queue.pop(0)
            directions = [[1,0],[-1,0],[0,1],[0,-1]]

            for l,r in directions:
                if x+l < self.size and y+r < self.size and (x+l,y+r) not in visited:
                    if origin in state[x+l][y+r]:
                        return cost
                    queue.append((x+l,y+r))
                    visited.add((x+l,y+r))

            cost += 1

        return cost




import time
fh = open("../tests/pub01.dat", 'r')
rtb = RTBProblem()
rtb.load(fh)
start = time.time()
print("SOLUTION:\n", search.astar_search(rtb))
end = time.time()
print("\ntime1 = ", end - start)

start = time.time()
print("SOLUTION:\n", search.uniform_cost_search(rtb))
end = time.time()
print("\ntime2 = ", end - start)