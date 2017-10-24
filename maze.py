from enum import IntEnum
from random import choice, randint

class D(IntEnum):
    N = 0
    E = 1
    S = 2
    W = 3

def opp(d): return (d + 2) % 4

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get(self, arr): return arr[self.y][self.x]

    def adj(self, d):
        if   d == D.N: return Point(self.x, self.y - 1)
        elif d == D.E: return Point(self.x + 1, self.y)
        elif d == D.S: return Point(self.x, self.y + 1)
        elif d == D.W: return Point(self.x - 1, self.y)
    def __repr__(self): return "(" + str(self.x) + ", " + str(self.y) + ")"

class Tile:
    def __init__(self):
        self.config = "1111"
    
    def get(self, d): 
        return self.config[d] == "1"

    def set(self, d, up): 
        flag = "1" if up else "0"
        self.config = self.config[:d] + flag + self.config[d+1:]
        return self
        
class Maze: 
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.maze = [[Tile() for x in range(w)] for y in range(h)]

    def get(self, p, d):
        a = p.get(self.maze)
        b = p.adj(d).get(self.maze)
        return (a, b)

    def set(self, p, d, wall):
        if self.in_bounds(p) and self.in_bounds(p.adj(d)):
            a, b = self.get(p, d)
            a.set(d, wall)       
            b.set(opp(d), wall)
        return self

    def is_wall(self, p, d):
        a, b = self.get(p, d)
        return a.get(d) and b.get(opp(d))

    def create(self, p, d):
        self.set(p, d, True)
        return self

    def carve(self, p, d):
        self.set(p, d, False)
        return self

    def in_bounds(self, p):
        return (p.x >= 0 and p.x < self.w and p.y >= 0 and p.y < self.h)

    def rand_neighbor(self, p):
        while True: 
            a = p.adj(choice(list(D)))
            if self.in_bounds(a): break
        return a

    def rand_point(self):
        while True:
            x = randint(0, self.w - 1)
            y = randint(0, self.h - 1)
            p = Point(x, y)
            if self.in_bounds(p): break
        return p

    def __repr__(self):
        line = "-----".join(["+" for tile in range(self.w + 1)]) + "\n"
        rep = line
        for row in self.maze: 
            v = "     ".join(["|" if tile.get(D.W) else " " for tile in row]) + "     |\n"
            h = "+" + "+".join(["-----" if tile.get(D.S) else "     " for tile in row]) + "+\n"
            rep = rep + v*2 + h
        return rep

if __name__ == "__main__":
    m = Maze(5, 5) 
    print(m.carve(Point(1, 1), D.W).carve(Point(3, 0), D.S))
