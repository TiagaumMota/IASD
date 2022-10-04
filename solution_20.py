import search

class RTBProblem(search.Problem):

    def __init__(self):
        self.size    = None
        self.xy_init = None
        self.xy_goal = None
        self.puzzle  = []

    def load(self, fh) -> None:

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
        self.puzzle = puzzle

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
    def getTileString(self, x: int, y: int):
        return self.puzzle[x][y]      

    def isSolution(self) -> int:
        
        # Searching and saving the starting tile's coordinates
        count_init = 0
        count_goal = 0
        for x in range(self.size):
            for y in range(self.size):
                if ("initial" in self.puzzle[x][y]):
                    self.xy_init = [x, y]
                    count_init += 1
                elif ("goal" in self.puzzle[x][y]):
                    self.xy_goal = [x, y]
                    count_goal += 1
        
        # Checking if the puzzle has a single starting and ending tile
        if (count_init != 1 and count_goal != 1):
            return 0
        
        # Saving initial tile's coordinates
        x_init = self.xy_init[0]
        y_init = self.xy_init[1]
        
        direction = None
        origin    = None
        tile      = None

        # Catching the string of the starting tile
        tile_init = self.puzzle[x_init][y_init]

        # Gathering the direction of the starting tile
        direction = self.getNextDirection(tile_init, "")

        # Also saving where the starting tile is positioned in relation to the tile it is pointing at
        origin = self.getNextOrigin(direction)

        # Initial row and collumn are the ones of the starting tile
        row = x_init
        col = y_init

        while (True):

            # Try catch detects if the path tiles lead to leaving the boundaries of the puzzle
            try:
                # Computing the next tile's coordinates
                (row, col) = self.getNextCoords(row, col, direction)

                # Gathering next tile's string
                tile = self.getTileString(row, col)

                # Checking if origin is in this new tile
                if origin not in tile:
                    return 0
                # Checking if this new tile is the goal
                elif "goal" in tile:
                    return 1
                else:
                    # Compute direction for the next tile
                    direction = self.getNextDirection(tile, origin)

                    # Save the origin tile to know where we were
                    origin = self.getNextOrigin(direction)

            except:
               return 0
