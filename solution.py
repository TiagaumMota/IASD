import search

class RTBProblem(search.Problem):

    def __init__(self):
        self.initial = None
        self.final = None
        self.puzzle = None
        self.size = None

    def load(self, fh) -> None:
        
        lines = [line.replace("\n", "") for line in fh.readlines() if "#" not in line]
        self.size = int(lines[0])
        print(lines)
        
    def is_solution(self) -> int:
        pass





if __name__ == "__main__":
    
    with open("pub07.dat", "r") as f:
        RTBProblem().load(f)
