import search

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

        '''for l in self.puzzle:
            print(l)
        print(self.initial)
        print(self.final)'''
        
    def is_solution(self) -> int:
        
        initial = self.puzzle[self.initial[0]][self.initial[1]]
        print(initial)


class Tile:
    
    def __init__(self, text: str) -> None:
        self.text = text

    def __repr__(self):
        return self.text


if __name__ == "__main__":
    
    with open("pub03.dat", "r") as f:
        t = RTBProblem()
        t.load(f)

    t.is_solution()