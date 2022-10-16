from mimetypes import init
import search

class Tile:
    
    def __init__(self, text: str) -> None:
        self.text = text

    def __repr__(self):
        return self.text

class RTBProblem(search.Problem):

    def __init__(self):
        self.initial = None
        self.final = None
        self.puzzle = []
        self.size = None

    def load(self, fh) -> None:
        
        lines = [line.replace("\n", "") for line in fh.readlines() if "#" not in line]
        self.size = int(lines[0])

        for i,line in enumerate(lines[1:]):
            temp_list = []
            for j,temp in enumerate(line.split()):

                temp_list.append(Tile(temp))

                if "initial" in temp:
                    self.initial = (i,j)
                elif "goal" in temp:
                    self.final = (i,j)

            self.puzzle.append(temp_list)
    
    def next_direction(self, tile: Tile, origin: str) -> str:

        l = tile.text.split("-")
        l.remove(origin)

        if "right" in l:
            return "right"
        elif "left" in l:
            return "left"
        elif "top" in l:
            return "top"
        elif "down" in l:
            return "down"

    def isSolution(self) -> int:
        
        initial = self.puzzle[self.initial[0]][self.initial[1]]

        if "right" in initial.text:
            next_tile_pos = (self.initial[0], self.initial[1]+1)
            origin = "left"
        elif "left" in initial.text:
            next_tile_pos = (self.initial[0], self.initial[1]-1)
            origin = "right"
        elif "top" in initial.text:
            next_tile_pos = (self.initial[0]-1, self.initial[1])
            origin = "down"
        elif "down" in initial.text:
            next_tile_pos = (self.initial[0]+1, self.initial[1])
            origin = "top"


        while(True):
            try:
                next_tile = self.puzzle[next_tile_pos[0]][next_tile_pos[1]]

                if origin not in next_tile.text:
                    return 0
                elif "goal" in next_tile.text:
                    return 1
                else:

                    direction = self.next_direction(next_tile, origin)

                    if "right" in direction:
                        next_tile_pos = (next_tile_pos[0], next_tile_pos[1]+1)
                        origin = "left"
                    elif "left" in direction:
                        next_tile_pos = (next_tile_pos[0], next_tile_pos[1]-1)
                        origin = "right"
                    elif "top" in direction:
                        next_tile_pos = (next_tile_pos[0]-1, next_tile_pos[1])
                        origin = "down"
                    elif "down" in direction:
                        next_tile_pos = (next_tile_pos[0]+1, next_tile_pos[1])
                        origin = "top"

            except Exception as e:
                return 0